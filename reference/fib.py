# Fibonacci sequence - first 15 numbers
def fibonacci(n):
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# Print first 15 Fibonacci numbers
first_15 = fibonacci(15)
print("First 15 Fibonacci numbers:")
print(first_15)