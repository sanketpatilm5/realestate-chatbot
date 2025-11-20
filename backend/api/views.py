from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .data_loader import get_dataset
import numpy as np
import re

def api_home(request):
    return JsonResponse({'message': 'Real Estate Chatbot API is running.'})


# 🔹 Smart Natural Language Intent and Area Extraction
def detect_intent(query: str):
    q = query.lower()

    # Detect metric
    if "demand" in q:
        metric = "demand"
    elif "price" in q or "rate" in q or "growth" in q:
        metric = "price"
    else:
        metric = "mixed"

    # ⚙ Improved area cleanup (handles trailing S, numbers, extra words)
    def clean_area(name):
        name = re.sub(r'\b(demand|price|trend|trends|growth|units|sales|chart|analysis|analyze)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\b(compare|and|vs|over|the|last|years|year|for|of|in|show)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\d+', '', name)  # Remove numbers like "3" from "Akurdi 3"
        name = re.sub(r'\s+', ' ', name)  # Remove extra spaces
        return name.strip().title()

    # 🔸 Comparison logic
    if "compare" in q and " and " in q:
        part = q.split("compare", 1)[1]
        left, right = [clean_area(x) for x in part.split(" and ", 1)]
        return "compare", metric, [left, right]

    if " vs " in q:
        left, right = [clean_area(x) for x in q.split(" vs ", 1)]
        return "compare", metric, [left, right]

    # 🔹 Single area logic
    tokens = q.replace("analysis", "").replace("analyze", "").replace("show", "").split()
    if "of" in tokens:
        area_guess = " ".join(tokens[tokens.index("of") + 1:])
    elif "in" in tokens:
        area_guess = " ".join(tokens[tokens.index("in") + 1:])
    elif "for" in tokens:
        area_guess = " ".join(tokens[tokens.index("for") + 1:])
    else:
        area_guess = " ".join(tokens[-2:])  # Last 2 words

    return "single", metric, [clean_area(area_guess)]


# 🧠 Summary generator
def build_single_area_summary(df_area, area, metric):
    years = sorted(df_area["year"].unique().tolist())
    total_sales = float(df_area["total_sales - igr"].sum())
    demand_total = int(df_area["total sold - igr"].sum())

    if metric == "price":
        metric_text = "price trend"
    elif metric == "demand":
        metric_text = "demand trend"
    else:
        metric_text = "overall trend"

    return (
        f"For {area}, data is available from {years[0]} to {years[-1]}. "
        f"Total sales were approximately ₹{total_sales:,.0f}, "
        f"with {demand_total} units sold. "
        f"This suggests a strong {metric_text}, visible in the chart."
    )


# 📈 Chart builder
def build_chart(df_area, area, metric, compare_mode=False):
    col = "total sold - igr" if metric == "demand" else "total_sales - igr"
    label_suffix = "Demand (Units Sold)" if metric == "demand" else "Total Sales"

    grouped = df_area.groupby("year")[col].sum().reset_index().sort_values("year")
    return {
        "labels": grouped["year"].astype(int).tolist(),
        "datasets": [{
            "label": f"{area} - {label_suffix}" if not compare_mode else label_suffix,
            "data": grouped[col].tolist(),
        }],
    }


# 📊 Table builder
def build_table(df_area):
    cols = [
        "final location", "year", "city",
        "total_sales - igr", "total sold - igr",
        "total units", "total carpet area supplied (sqft)",
    ]
    return df_area[[c for c in cols if c in df_area.columns]].sort_values("year").to_dict(orient="records")


# 🚀 Main query processor
class ChatAnalyzeView(APIView):
    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "Query is required."}, status=400)

        df = get_dataset()
        intent, metric, areas = detect_intent(query)

        if not areas:
            return Response({"error": "Could not detect location."}, status=400)

        # 🔥 SINGLE AREA
        if intent == "single":
            area = areas[0]
            df_area = df[df["final location"].str.lower().str.strip().str.contains(area.lower())]

            if df_area.empty:
                return Response({"error": f"No data found for '{area}'."}, status=404)

            # Handle "last X years"
            if "last" in query.lower():
                match = re.search(r'last (\d+) year', query.lower())
                if match:
                    years_back = int(match.group(1))
                    max_year = df_area["year"].max()
                    df_filtered = df_area[df_area["year"] >= max_year - years_back + 1]
                    if not df_filtered.empty:
                        df_area = df_filtered

            return Response({
                "query": query,
                "mode": "single",
                "area": area,
                "summary": build_single_area_summary(df_area, area, metric),
                "chart": build_chart(df_area, area, metric),
                "table": build_table(df_area),
            })

        # 🔥 COMPARISON
        elif intent == "compare":
            area1, area2 = areas
            df1 = df[df["final location"].str.lower().str.strip().str.contains(area1.lower())]
            df2 = df[df["final location"].str.lower().str.strip().str.contains(area2.lower())]

            if df1.empty or df2.empty:
                return Response({"error": f"Data not found for areas: {area1}, {area2}"}, status=404)

            if "last" in query.lower():
                match = re.search(r'last (\d+) year', query.lower())
                if match:
                    years_back = int(match.group(1))
                    max_year = max(df1["year"].max(), df2["year"].max())
                    df1_filtered = df1[df1["year"] >= max_year - years_back + 1]
                    df2_filtered = df2[df2["year"] >= max_year - years_back + 1]
                    if not df1_filtered.empty:
                        df1 = df1_filtered
                    if not df2_filtered.empty:
                        df2 = df2_filtered

            col = "total sold - igr" if metric == "demand" else "total_sales - igr"
            label_suffix = "Demand (Units Sold)" if metric == "demand" else "Total Sales"
            labels = sorted(set(df1["year"]).union(df2["year"]))

            def align(df_data):
                data = df_data.groupby("year")[col].sum()
                return [data.get(year, np.nan) for year in labels]

            return Response({
                "query": query,
                "mode": "compare",
                "areas": [area1, area2],
                "summary": f"Comparison between {area1} and {area2} showing {label_suffix.lower()} trends.",
                "chart": {
                    "labels": labels,
                    "datasets": [
                        {"label": f"{area1} - {label_suffix}", "data": align(df1)},
                        {"label": f"{area2} - {label_suffix}", "data": align(df2)},
                    ],
                },
                "tables": {
                    area1: build_table(df1),
                    area2: build_table(df2),
                },
            })

        return Response({"error": "Unable to process query."}, status=400)
