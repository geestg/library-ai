def calculate_gap_score(

    method_gap,

    dataset_gap,

    temporal_gap,

    evaluation_gap

):

    return min(

        100,

        (

            len(method_gap) * 10

            +

            len(dataset_gap) * 10

            +

            len(temporal_gap) * 15

            +

            len(evaluation_gap) * 20
        )
    )

