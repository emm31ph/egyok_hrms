import click

from egyok_hrms.setup import after_install as setup


def after_install():
	try:
		print("Setting up Frappe EGYOK HRMS...")
		setup()

		click.secho("Thank you for installing Frappe EGYOK HRMS!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/emm31ph/egyok_hrms/issues/new"
		click.secho(
			"Installation for Frappe EGYOK HRMS app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e