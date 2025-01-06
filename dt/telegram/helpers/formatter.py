from typing import Optional


def format_html_job_listing(job: dict, category: Optional[str] = None) -> str:
    """Format a job listing for display."""
    job_title = job["title"]
    job_company = job["company"]
    job_location = job["location"]
    job_description = job["description"]
    job_description = (
        job_description[:50] + "..."
        if len(job_description) > 50
        else job_description
    )
    job_link = job["link"]
    separator = "<code>-------------------------</code>"
    job_description = job_description.replace("\n\n", " ")
    job_description = job_description.replace("\n\n\n", " ")
    category = f"Subscription: {category}\n" if category else ""
    return (
        f"<b> 💼 {job_title}</b>\n"
        f"<i>{job_company} - {job_location}</i>\n"
        f"{job_description}\n"
        f"<a href='{job_link}'>View Job</a>\n"
        f"{category}"
        f"{separator}"
    )
