def format_html_job_listing(job: dict) -> str:
    """Format a job listing for display."""
    return (
        f"<b> 💼 {job['title']}</b>\n"
        f"<i>{job['company']} - {job['location']}</i>\n"
        f"{job['description']}\n"
        f"<a href='{job['link']}'>View Job</a>\n"
        "-----------------------------------"
    )
