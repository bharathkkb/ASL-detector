from celeryTask import *

result = add.delay(23, 42)
result.wait()  # 65
print(result.get())
