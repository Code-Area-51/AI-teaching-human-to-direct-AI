import argparse
import sys
from src.utils import ActionHandler, logger
from src.cleaner import SystemCleaner
from src.organizer import FileOrganizer
from src.reporter import SystemReporter

def main():
    parser = argparse.ArgumentParser(description="Windows System Health & Cleanup Assistant")
    
    # Action arguments
    parser.add_argument('--clean', action='store_true', help='Clean temp files, logs, and browser caches.')
    parser.add_argument('--organize', action='store_true', help='Organize Desktop and Downloads folders.')
    parser.add_argument('--report', action='store_true', help='Generate a system health report.')
    
    # Safety arguments
    parser.add_argument('--dry-run', action='store_true', default=True, help='List actions without executing them (Default).')
    parser.add_argument('--no-dry-run', action='store_false', dest='dry_run', help='Execute actions (Delete/Move files).')
    
    args = parser.parse_args()

    # Determine execution mode
    dry_run = args.dry_run
    if dry_run:
        logger.info("Running in DRY RUN mode. No files will be changed.")
    else:
        logger.warning("Running in LIVE mode. Files WILL be modified/deleted.")

    # Initialize Action Handler
    action_handler = ActionHandler(dry_run=dry_run)

    # 1. Cleaner
    if args.clean:
        logger.info("Starting Cleanup Process...")
        cleaner = SystemCleaner(action_handler)
        count, freed_bytes = cleaner.run()
        from src.utils import format_size
        logger.info(f"Cleanup complete. Removed {count} items. Space freed: {format_size(freed_bytes)}")

    # 2. Organizer
    if args.organize:
        logger.info("Starting Organization Process...")
        organizer = FileOrganizer(action_handler)
        organizer.run()

    # 3. Report
    if args.report:
        logger.info("Generating System Report...")
        reporter = SystemReporter()
        print(reporter.generate_report())

    if not (args.clean or args.organize or args.report):
        parser.print_help()

if __name__ == '__main__':
    main()
