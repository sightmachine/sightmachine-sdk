# CVE Audit Task

There are 2 CVE audit tasks for the SDK build.

1. **Lightweight Repository Audit Report:**
   - This report provides information based on the repository build.
   - It is triggered on each commit and pull request (PR).
   - Focuses on essential information related to the repository's build status.

2. **Nightly Master Branch Audit Report:**
   - This report provides daily build-based information specifically for the master branch.
   - It runs nightly on the latest master branch.
   - Excludes container-based audit reporting as there is no associated container with the SDK.

The CVE audit report is conducted using a tool called [Trivy](https://trivy.dev/). The primary
configuration for the tool is [trivy.yaml](../trivy.yaml). Any unique global parameters for a
specific run are passed at execution.

The reporting tool currently only reports on CRITICAL & HIGH severity issues.
Vulnerability issues can further be filtered by status:

1. affected
2. fixed
3. will_not_fix
4. fix_deferred
5. end_of_life

Or by ID via a `.trivyignore` or `.trivyignore.yaml` file. Instructions for this can be found in the
[Trivy documentation](https://aquasecurity.github.io/trivy/v0.49/docs/configuration/filtering/).

## Trivy Template Information

The following links provide information on the Go-Template Engine within Trivy.

| Description                                 | Link                                                                   |
|---------------------------------------------|------------------------------------------------------------------------|
| Usage of Go-Templates in Trivy Command line | https://aquasecurity.github.io/trivy/v0.17.2/examples/report/#template |
| Go-Template Function list from Sprig        | https://masterminds.github.io/sprig/ |
| Trivy Code: wiring up function map          | https://github.com/aquasecurity/trivy/blob/v0.49.1/pkg/report/template.go#L31 |
| Trivy Code: passing data state to template  | https://github.com/aquasecurity/trivy/blob/v0.49.1/pkg/report/template.go#L79 |
