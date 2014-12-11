from __future__ import print_function
import sys
import os

VIEW_EXTENSION = ".cshtml"

FILES_TO_SEARCH = [".cshtml", "Controller.cs"]

def main(argv):
	directory = argv[0]

	views = find_view_files_in_directory(directory)

	print()
	print("Locating view files...")
	print()

	print("View files found:")
	print(views)
	print()

	print("Locating references...")
	print_break()

	for view_filename in views:

		print(view_filename)
		print()
		
		references = find_references_for_view_file(directory, view_filename)

		if not references:
			print("UNUSED VIEW: ", view_filename)
			print_break()
			continue
		
		for reference in references:
			print("line number: ", reference[1])
			print("line text: ", reference[2])
			print()
		print_break()


def print_break():
	print("----------------------")
	print()

def find_references_for_view_file(directory, viewfilename):
	references = []

	for root, directories, files in os.walk(directory):
		for filename in [f for f in files if any([f.endswith(ext) for ext in FILES_TO_SEARCH])]:
			with open(os.path.join(root, filename), 'r') as searchfile:
				linenumber = 0
				for line in searchfile:
					linenumber += 1
					if viewfilename in line:
						references.append((filename, linenumber, line))

	return references


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
