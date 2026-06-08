def process_arguments(*args):
    """
    This function takes multiple arguments, calculates their sum if they are numbers,
    and returns a dictionary with the original arguments and their sum.
    """
    result = {
        "original_arguments": args,
        "sum": sum(arg for arg in args if isinstance(arg, (int, float)))
    }
    return result

# Example usage
if __name__ == "__main__":
    output = process_arguments(1, 2, 3, "hello", 4.5)
    print(output)