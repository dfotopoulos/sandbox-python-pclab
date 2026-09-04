import argparse
import shlex
import sys

class ListManager:
    def __init__(self, data=None):
        self.data = data if data is not None else []

    def add(self, item):
        self.data.append(item)
        return self.data

    def remove(self, item):
        if item in self.data:
            self.data.remove(item)
        return self.data

    def sort(self):
        self.data.sort()
        return self.data

    def reverse(self):
        self.data.reverse()
        return self.data

    def pop(self):
        if self.data:
            return self.data.pop()
        return None

    def clear(self):
        self.data.clear()
        return self.data

def main(argv=None):
    if argv is None and len(sys.argv) == 2 and " " in sys.argv[1]:
        argv = shlex.split(sys.argv[1])
    elif argv is not None and len(argv) == 1 and " " in argv[0]:
        argv = shlex.split(argv[0])

    parser = argparse.ArgumentParser(description="Manipulate a list via CLI switches.")
    parser.add_argument("--data", nargs='*', default=[], help="Initial list elements (e.g. --data a b c)")
    parser.add_argument("--add", help="Add an item to the list")
    parser.add_argument("--remove", help="Remove an item from the list")
    parser.add_argument("--sort", action="store_true", help="Sort the list alphabetically")
    parser.add_argument("--reverse", action="store_true", help="Reverse the list order")
    parser.add_argument("--pop", action="store_true", help="Pop the last element")
    parser.add_argument("--clear", action="store_true", help="Clear the list")

    args = parser.parse_args(argv)
    manager = ListManager(args.data)

    if args.add is not None:
        print(f"Result: {manager.add(args.add)}")
    elif args.remove is not None:
        print(f"Result: {manager.remove(args.remove)}")
    elif args.sort:
        print(f"Result: {manager.sort()}")
    elif args.reverse:
        print(f"Result: {manager.reverse()}")
    elif args.pop:
        popped = manager.pop()
        print(f"Popped: {popped}, Remaining: {manager.data}")
    elif args.clear:
        print(f"Result: {manager.clear()}")
    else:
        print(f"Current List: {manager.data}")

if __name__ == "__main__":  # pragma: no cover
    main()
