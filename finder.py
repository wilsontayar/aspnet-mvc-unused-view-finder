import sys
import os

LOOKUP_EXTENSIONS = [".cshtml", ".gif", ".jpg", ".png", ".js", ".css"]
FILES_TO_SEARCH = [".cshtml", "Controller.cs", ".css", ".less", ".js"]

def main(argv):
	directory = argv[0]

	files_to_look_for = find_view_files_in_directory(directory)

	print_break()
	print("Loading files...")
	print_break()

	print("files to look for: {0}".format(len(files_to_look_for)))
	print_break()

	print("Looking for unused files...")
	print_break()

	results = {'using': [], 'not_using': []}

	for file_name in files_to_look_for:
		references, looked_at = find_references_for_view_file(directory, file_name)

		if not references:
			results['using'].append(file_name)
		else:
			results['not_using'].append(file_name)

	print("USING: {0} files".format(len(results['using'])))
	print("NOT USING: {0} files".format(len(results['not_using'])))
	for file in results['not_using']:
		print(file)

def print_break():
	print("-" * 45)

def find_references_for_view_file(directory, file_name):
	using = []
	looking_in = []

	for root, directories, files in os.walk(directory):
		for filename in [f for f in files if any([f.endswith(ext) for ext in FILES_TO_SEARCH])]:
			looking_in.append(os.path.join(root, filename))
			with open(os.path.join(root, filename), 'r', encoding="ISO-8859-1") as searchfile:
				content = searchfile.read()
				if file_name in content:
					using.append(filename)

	return (using, looking_in)


def find_view_files_in_directory(directory):
	views = []

	for root, directories, files in os.walk(directory):
		for ext in LOOKUP_EXTENSIONS:
			for filename in [f for f in files if f.endswith(ext)]:
				views.append(filename)

	return views

if __name__ == "__main__":
	if len(sys.argv) == 1:
		sys.exit("Argument required: application path")

	main(sys.argv[1:])
