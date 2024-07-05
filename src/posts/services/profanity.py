from profanity_check import predict


def detect_profanity(contents: [str]):
    predictions = predict(contents)
    contains_profanity = bool(max(predictions))
    return contains_profanity
