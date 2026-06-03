def build_chat_context(
        dataset, limit=500
):
    records=[
        {
            "sheet_name":record.sheet_name,
            "data":record.data
        }
        for record in dataset.all()[:limit]
    ]

    return {
        "record_count":len(records),
        "records":records
    }