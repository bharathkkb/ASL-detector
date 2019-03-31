from celeryTask import *

result = add_together.delay(23, 42)
result.wait()  # 65
print(result.get())
