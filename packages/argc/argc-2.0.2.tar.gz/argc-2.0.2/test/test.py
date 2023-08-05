from argc import argc, sys # import sys from module

if __name__ == "__main__":
    args = argc(sys.argv[1:], False) # sys.argv is default and detectType only works on python3 (off by default)

    args.add("--help", "\nThere is no helpª for you!\n", True) # exitOn (default off) exits when this argument is chosen 
    args.add("-func", lambda: 1 + 1, True) # can be used with /func and -func not --func

    args.run() # checks all arguments and runs apropriate actions (can exit)

    print(args.get("--set-version"))
