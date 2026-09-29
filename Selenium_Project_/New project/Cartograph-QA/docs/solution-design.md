# Capstone design record

## Phase 1 - official requirements

The supplied document's Assignment 4 explicitly requires: Robot Framework basics; SeleniumLibrary; RIDE IDE; keyword-driven testing; data-driven testing; resource files; user-defined keywords; setup and teardown; Page Object Model concept; Jenkins execution; command-line execution; reporting. Its scenario is an e-commerce web automation flow: launch browser, login, search product, add product to cart, verify cart, logout, close browser. Suggested applications are Automation Exercise and Demo Web Shop.

All other choices are optional: project name, website selection, directory conventions, browser, test data format, environment model, locator policy, report enhancement, retries, parallelism, CI parameter design, and GitHub presentation.

## Phase 2 - basic submission risk

A typical project would place locator strings, SeleniumLibrary keywords, credentials and a single happy-path case in one `.robot` file, then run `robot tests/`. It can satisfy the flow but is difficult to change, cannot safely demonstrate data/configuration choices, and gives weak failure context.

## Phases 3-5 - evaluated ideas

| Idea | Value / demonstration | Difficulty | Decision |
| --- | --- | --- | --- |
| Layered resources | Trace a test to facade, page, locator | Low | Selected |
| Business facade | Show executable business language | Low | Selected |
| JSON provider | Add a case without changing workflow | Low | Selected |
| Central configuration | Run browser/profile without test edit | Medium | Selected |
| Locator SSOT | Make one locator correction | Low | Selected |
| Screenshot evidence | Show failure PNG and native log | Low | Selected |
| Execution dashboard | Show concise summary + metadata | Medium | Selected |
| Parameterized Jenkins | Change build parameters | Medium | Selected |
| Cross-browser capability | Chrome/Firefox command | Low | Selected |
| Controlled retry | Explain any retry in report | Medium | Rejected: risks masking defects |
| Pabot parallelism | Compare build duration | Medium | Rejected: public app/shared account isolation risk |
| Docker | Same runner everywhere | Medium | Rejected: no demonstrated deployment problem |
| AI diagnostics | Natural-language triage | High | Rejected: non-deterministic and unnecessary |
| Database state | Seed/verify data | High | Rejected: unrelated to target site |

The selected eight are useful, uncommon in basic student work, moderate-to-low complexity, reliable, and easy to demonstrate. They strengthen mandatory requirements but are enhancements except Jenkins and the required architecture concepts they implement.

## Phases 6-8 - quality and traceability

The `Test -> Business -> Page -> Locator/Selenium` boundary prevents tests from knowing UI implementation. `ConfigProvider` is the execution strategy boundary; CLI values override its default profile. `DataProvider` is the data-factory boundary. Each test has a fresh browser session, its own setup and teardown, explicit waits, and no fixed sleeps.

| Official requirement | Where implemented | Demonstration | Status |
| --- | --- | --- | --- |
| Robot Framework Basics | `tests/data_driven_cart.robot` | Run suite | Ready |
| SeleniumLibrary | page/framework resources | Show browser journey | Ready |
| RIDE IDE | README setup/checklist | Open suite/resources in RIDE | Needs local installation |
| Keyword-Driven Testing | `business_flows.resource` | Read business journey | Ready |
| Data-Driven Testing | JSON + `DataProvider.py` + template | Three dataset executions | Ready |
| Resource Files | `resources/**/*.resource` | Imports in suite | Ready |
| User Defined Keywords | page/business/framework keywords | Navigate definitions | Ready |
| Setup & Teardown | test setup/teardown in suite | Browser/evidence lifecycle | Ready |
| POM Concept | locator/page/business separation | Show folder layers | Ready |
| Jenkins Execution | `Jenkinsfile` | Parameterized pipeline | Needs Jenkins agent/credentials |
| Command Line Execution | README commands | Run `robot` | Ready after dependencies/config |
| Reporting | native reports + summary generator | Open result folder | Ready after execution |

## Phase 9 - GitHub readiness

Before publishing: replace team placeholders, add team-owned screenshots/GIF after a real run, add a license only when approved, and keep `.env` out of version control. The root `README.md`, `.gitignore`, Jenkinsfile, architecture diagram, configuration/data instructions and reporting documentation are included.

## Phase 10 - final quality gate

| Check | Result |
| --- | --- |
| Internal imports and referenced paths | Ready - checked by static inspection |
| Undefined variables/keywords | Ready - variables are supplied by providers or Robot built-ins |
| Locator duplication | Ready - centralized locator resources |
| Hard-coded credentials | Ready - only placeholders; secret sourced from `.env`/CI |
| Fixed sleeps / fragile timing | Ready - explicit waits, no sleeps |
| Teardown/evidence | Ready - per-test diagnostic then close |
| Cross-browser execution | Needs configuration - Firefox must be installed to demonstrate it |
| Live UI locator validity | Needs configuration/verification - public UI can change and a real test account is required |
| Jenkins | Needs configuration - Windows agent, plugins, credentials required |
| GitHub secrets | Ready if `.env` remains untracked |
| RIDE | Needs configuration - install/verify in your Python environment |

No item is marked "must be fixed" in the checked-in framework. A live run is intentionally not claimed until the team supplies the dedicated account and local browser environment.
