from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

import json
from .models import Dataset, DataRecord
from .serializers import DatasetSerializer
from .utils import parse_excel
from analytics.tasks import process_dataset_task


import math
from datetime import datetime, date
from decimal import Decimal

def clean_row(row):
    cleaned = {}

    for k, v in row.items():

        # Handle datetime
        if isinstance(v, (datetime, date)):
            cleaned[k] = v.isoformat()

        # Handle Decimal
        elif isinstance(v, Decimal):
            cleaned[k] = float(v)

        # Handle NaN / Infinity
        elif isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            cleaned[k] = None

        # Handle normal JSON-safe types
        elif isinstance(v, (int, float, str, bool)) or v is None:
            cleaned[k] = v

        # Fallback (VERY important)
        else:
            cleaned[k] = str(v)

    return cleaned

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    serializer = DatasetSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Save dataset
            dataset = serializer.save(user=request.user)

            # Parse file
            parsed_data = parse_excel(dataset.file)

            # Save records safely
            records = []
            for row in parsed_data:
                clean_data = clean_row(row)
                records.append(DataRecord(dataset=dataset, data=clean_data))

            DataRecord.objects.bulk_create(records)

            # Trigger processing AFTER records exist
            process_dataset_task.delay(dataset.id)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Re-serialize saved instance
    response_data = DatasetSerializer(dataset).data

    return Response(response_data, status=status.HTTP_201_CREATED)