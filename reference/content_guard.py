def require(ok, code):
    if not ok:
        raise ValueError(code)

def validate_api_content(comparison, policy):
    require(policy.get("activeApiIdentity") == "verified-archive-filesystem-tree-v1",
            "api_filesystem_identity_not_reviewed")
    require(comparison.get("fileContentsMatch") is True
            and comparison.get("directoryTreeMatch") is True, "active_api_filesystem_mismatch")
