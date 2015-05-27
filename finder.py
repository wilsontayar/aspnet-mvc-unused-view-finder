import sys
import os

VIEW_EXTENSION = ".cshtml"

FILES_TO_SEARCH = [".cshtml", "Controller.cs"]

def main(argv):
	directory = argv[0]

	views = find_view_files_in_directory(directory)

	print("Locating view files...")
	print_break()

	print("View files found: {0}".format(len(views)))
	print_break()

	print("Finding unused views...")
	print_break()

	for view_filename in views:
		references, looked_at = find_references_for_view_file(directory, view_filename)

		if not references:
			print("UNUSED VIEW: ", view_filename)
			print_break()

def print_break():
	print("-" * 45)

def find_references_for_view_file(directory, viewfilename):
	references = []
	looking_in = []

	for root, directories, files in os.walk(directory):
		for filename in [f for f in files if any([f.endswith(ext) for ext in FILES_TO_SEARCH]) and not f == viewfilename + VIEW_EXTENSION]:
			looking_in.append(os.path.join(root, filename))
			with open(os.path.join(root, filename), 'r', encoding="utf-8") as searchfile:
				linenumber = 0
				for line in searchfile:
					linenumber += 1
					if viewfilename in line :
						references.append((filename, linenumber, line))

	return (references, looking_in)


def find_view_files_in_directory(directory):
	views = []

	for root, directories, files in os.walk(directory):
		for filename in [f for f in files if f.endswith(VIEW_EXTENSION)]:
			views.append(filename.replace(VIEW_EXTENSION, ""))

	return views

if __name__ == "__main__":
	if len(sys.argv) == 1:
		sys.exit("Argument required: application path")

	main(sys.argv[1:])
