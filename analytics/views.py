from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset,AnalysisResult,FailedRow


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dataset_status(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    return Response({
        "id": dataset.id,
        "name": dataset.name,
        "status": dataset.status,
        "progress": getattr(dataset, "progress", 0),
        "uploaded_at": dataset.uploaded_at,
    })



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analysis(request,dataset_id):

    try:
        dataset =Dataset.objects.get(
            id=dataset_id,
            user=request.user
        )
    except Dataset.DoesNotExist:
        return Response(
            {"error":"Dataset not found"},
            status=404
        )
    try:
        analysis=AnalysisResult.objects.get(dataset=dataset)
    except AnalysisResult.DoesNotExist:
        return Response ({"error":" No analysis found"},
        status=404
        )
    
    return Response(
        {
            "dataset_id":dataset.id,
            "summary":analysis.summary,
            "created_at":analysis.created_at
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_failed_rows(request,dataset_id):

    try: 
        dataset=Dataset.objects.get(
            id=dataset_id,
            user=request.user
        )

    except Dataset.DoesNotExist:
        return Response(
            {"error":"Dataset not found"},
            status=404
        )
    failed_rows=FailedRow.objects.filter(
        dataset=dataset

    ).order_by("-created_at")

    data =[]

    for row in failed_rows:
        data.append({
            "id":row.id,
            "raw_data":row.raw_data,
            "error":row.error,
            "created_at":row.created_at
        })

    return Response(data)