"""
Example of how users will use the compiled package
"""
import secretpackage

print("Testing secretpackage functionality:\n")

# Math utilities
print("Math utilities:")
print(f"add(5, 3) = {secretpackage.add(5, 3)}")
print(f"multiply(4, 7) = {secretpackage.multiply(4, 7)}")
print(f"power(2, 8) = {secretpackage.power(2, 8)}")

# String utilities
print("\nString utilities:")
print(f"reverse_string('hello') = {secretpackage.reverse_string('hello')}")
print(f"capitalize_words('hello world') = {secretpackage.capitalize_words('hello world')}")
print(f"remove_spaces('hello world') = {secretpackage.remove_spaces('hello world')}")

# Data utilities
print("\nData utilities:")
print(f"process_list([3, 1, 4, 1, 5, 9]) = {secretpackage.process_list([3, 1, 4, 1, 5, 9])}")
max_val, min_val = secretpackage.find_max_min([1, 2, 3, 4, 5])
print(f"find_max_min([1, 2, 3, 4, 5]) = max: {max_val}, min: {min_val}")
print(f"calculate_average([1, 2, 3, 4, 5]) = {secretpackage.calculate_average([1, 2, 3, 4, 5])}")

print(f"\nPackage version: {secretpackage.__version__}")