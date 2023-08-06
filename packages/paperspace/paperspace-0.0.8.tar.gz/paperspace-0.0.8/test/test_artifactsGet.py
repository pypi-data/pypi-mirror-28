import paperspace

print("paperspace.jobs.artifactsGet({'jobId': 'jskhh3k4o9jsrn', 'dest': '~/temp1'}, no_logging=True)")
files = paperspace.jobs.artifactsGet({'jobId': 'jskhh3k4o9jsrn', 'dest': '~/temp1'}, no_logging=True)
paperspace.print_json_pretty(files)
