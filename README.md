# healthy-xjtuer

Use github action to help you complete the dummy daily health report.

## Usage

1. Fork this repo.
2. Add netid and password in repositories `Secrets`.
3. The check-in task will be automatically executed at 12:00 UTC+8. It could be modified in [check-in.yml](.github/workflows/check-in.yml).
4. The job will also be triggered on push action.
5. You may need to run the action manually once to trigger the daily task.

## Todo

- [ ] add graduate student check-in support

## Declaration

Please note that this project is for personal practice only and no technical support is provided. Under no circumstances are we encouraged to use this project to complete the daily health form. Use at your own risk.

## License

MIT License
