import sys
import sqlbrowser

print()
instances = sqlbrowser.get_instances(sys.argv[1])
for i in instances:
    for k in i.keys():
        print(f"{k}: {i[k]}")
    print()
