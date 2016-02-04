match_patterns = [
    ("^(.*)(\"\,\"secret-key\":\")(.*)(\"\}\\\\n)", 2),
    ("^(.*)(\"\,\\\"secret-key\\\"\:\\\")(.*)(\"\}\\\\)(.*)", 3),
    ("^(\s.*\"secret-key\" \: \")(.*)(\")", 2),
    ("^(.*)(.engine.files\" \: \")(.*)(\"\,)", 3),
    ("^(.*)(Checking if file \')(.*)(\' already exists)", 3),
    ("^(.*)(recursive stat for \:\s)(.*)", 3),
    ("^(.*)(Attempt\s[0-9].*\sfor\s)(.*)(\ssuccessfully handled response)", 3),
    ("^(.*)(Attempt\s[0-9].*\sfor\s)(.*)(\sfailed to handle response)", 3),
    ("^(.*)(Attempt\s[0-9].*\sfor\s)(.*)(\sfinal failure to handle response)", 3),
    ("^(.*)(found for:\s)(.*)(\serror code:)(.*)", 3),
    ("^(.*)(Checking Folder\:\s)(.*)", 3),
    ("^(.*)(folder for\s\:\s)(.*)", 3),
    ("^(.*)(List for filter =\s)(.*)(\, delimiter)(.*)", 3),
    ("^(.*)(\&prefix\=)(.*)", 3),
    ("^(.*)(for folder check\s\:)(.*)", 3),
    ("^(.*)(\[DDSManifestExchangeConsumer-INFO\]\s)(.*)( file does not)(.*)", 3),
    ("^(.*)(file name:\s)(.*)(\,\sfile size)(.*)", 3),
    ("^(.*)(stream for file-system:\s)(.*)", 3),
    ("^(.*)(writer for file:\s)(.*)(\s\,\skey\:[0-9].*)", 3),
    ("^(.*)(Object parsed:\s)(.*)", 3),
    ("^(.*)(for \(https\),)(.*)", 3),
    ("^(.*)(Closing\s)(.*)", 3),
    ("^(.*)(BaseRestRequest: Attempt [0-9]* for\s)(.*)(\ssuccessfully handled response)", 3),
    ("^(.*)(Completed\s)(.*)", 3),
    ("^(.*)(of part [0-9]*\sof\s)(.*)(\scompleted without errors\.)", 3),
    ("^(.*)(Sent DE_FILE_COMPLETE\([0-9]*\)\s)(.*)", 3),
    ("^(.*)(Receive rate for\s)(.*)(\s= [0-9].* .bps.)", 3),
    ("^(.*)(Retrying file \')(.*)(' \([0-9].*\))", 3),
    ("^(.*)(\sDownloaded\s)(.*)(\sat\: [0-9].* .bps)", 3),
    ("^(.*)(-ERROR] File\s\')(.*)(\' was not found)", 3),
    ("^(.*)(results found for\:\s)(.*)(\, error code\: [0-9].*\, http code\: [0-9].*)", 3)
]
