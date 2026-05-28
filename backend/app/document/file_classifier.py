def classify_file(filename):

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return "pdf"

    if filename.endswith(".png"):
        return "image"

    if filename.endswith(".jpg"):
        return "image"

    if filename.endswith(".jpeg"):
        return "image"

    return "unknown"