def unique_keep_order(
    items
):

    seen = set()

    result = []

    for item in items:

        if item in seen:
            continue

        seen.add(item)

        result.append(item)

    return result


def get_dominant_items(
    frequency_dict: dict,
    threshold: int = 3
):

    return [

        name

        for name, count

        in frequency_dict.items()

        if count >= threshold
    ]


def get_emerging_items(
    frequency_dict: dict
):

    return [

        name

        for name, count

        in frequency_dict.items()

        if count == 2
    ]


def get_rare_items(
    frequency_dict: dict
):

    return [

        name

        for name, count

        in frequency_dict.items()

        if count == 1
    ]