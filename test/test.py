# 假设 results 是 fetchall() 返回的结果
results = [
    (1, 'Alice', 30),
    (2, 'Bob', 25)
]

# 将结果转换为字符串
result_strings = [' | '.join(map(str, row)) for row in results]

# 将所有行拼接成一个字符串，使用换行符分隔
final_string = '\n'.join(result_strings)

print(final_string)