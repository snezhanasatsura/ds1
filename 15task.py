
num = [3, 1, 9, -5, 7]

def find_min_max(numbers):
    if not numbers:
        raise ValueError("Список не должен быть пустым")

    min_value = numbers[0]
    max_value = numbers[0]

    for n in numbers:
        if n < min_value:
            min_value = n
        if n > max_value:
            max_value = n

    return min_value, max_value


result = find_min_max(num)
print(result)  # (-5, 9)