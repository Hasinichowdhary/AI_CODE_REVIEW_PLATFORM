from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CodeReview


@api_view(["GET"])
def home(request):
    return Response({
        "message": "AI Code Review API is working!"
    })


@api_view(["GET"])
def reviews(request):
    data = []

    for review in CodeReview.objects.all().order_by("-created_at"):
        data.append({
            "id": review.id,
            "code": review.code,
            "review": review.review,
            "created_at": review.created_at
        })

    return Response(data)


@api_view(["POST"])
def save_review(request):
    code = request.data.get("code")
    review = request.data.get("review")

    if not code or not review:
        return Response(
            {"error": "Code and review are required"},
            status=400
        )

    saved = CodeReview.objects.create(
        code=code,
        review=review
    )

    return Response({
        "message": "Review saved successfully!",
        "id": saved.id
    })