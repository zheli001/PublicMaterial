# Condo Application Package Creation Pipeline

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your/repo/releases)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/your/repo/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)
[![Last Updated](https://img.shields.io/badge/last--updated-2025--11--16-brightgreen)](#changelog)

## Overview

This pipeline automates the creation of customized condo application packages for realtors. It processes builder-provided materials (PDFs, videos, images, forms) and builder website information to create professional, branded application packages for potential clients.

## Key Features

- **Multi-format Material Processing**: Handles PDFs, videos, images, and application forms
- **Website Integration**: Extracts additional project information from builder websites
- **Agent Customization**: Automatically identifies and highlights sections requiring agent information
- **Quality Validation**: Ensures package completeness before client distribution
- **Professional Packaging**: Creates client-ready application packages with clear instructions

## Quick Start

### Prerequisites
- Builder materials directory containing PDFs, videos, images, and forms
- Builder website URL for additional project information
- Agent contact information and branding requirements

### Input Requirements
- **builder_materials_directory**: Directory containing all builder-provided materials
- **builder_website_url**: URL of the builder's project website

### Usage

1. **Prepare Materials**:
   ```bash
   # Place builder materials in a directory
   mkdir builder_materials
   # Copy PDFs, videos, images, forms to builder_materials/
   ```

2. **Configure Pipeline**:
   - Update `pipeline_template.yaml` with project-specific information
   - Set builder website URL and material directory paths

3. **Execute Pipeline**:
   ```bash
   # Run the pipeline (implementation depends on your pipeline executor)
   ./run_pipeline.sh pipeline_template.yaml
   ```

4. **Review Output**:
   - Check `artifacts/` directory for processed materials
   - Review `validation_report` for completeness
   - Use `client_ready_package` for distribution

## Pipeline Structure

### Phase 0: Material Collection & Analysis
1. **Gather Builder Materials** - Inventory and categorize all provided materials
2. **Analyze Builder Website** - Extract project specifications and additional resources
3. **Identify Customization Requirements** - Map all locations needing agent information

### Phase 1: Material Processing & Customization (Parallel)
1. **Process PDF Documents** - Customize PDFs with agent info and highlight changes
2. **Process Video Content** - Organize and catalog video materials
3. **Process Image Assets** - Optimize and organize image galleries
4. **Customize Application Forms** - Insert agent information and create completion guides

### Phase 2: Package Assembly & Validation
1. **Assemble Application Package** - Compile all materials into organized structure
2. **Validate Package Completeness** - Verify all requirements are met
3. **Prepare for Client Distribution** - Create professional packaging and instructions

## Output Structure

```
client_ready_package/
├── documents/
│   ├── customized_pdfs/
│   ├── application_forms/
│   └── completion_guides/
├── media/
│   ├── videos/
│   └── images/
├── manifest.txt
├── customization_highlights.pdf
└── README_for_client.md
```

## Configuration

### Pipeline Configuration
Edit `pipeline_template.yaml` to customize:

```yaml
config:
  root: "demo/condo"
  artifacts_base: "demo/condo/artifacts"
```

### Agent Information
Update agent details in the pipeline prompts or create a separate agent config file.

## Validation & Quality Checks

The pipeline includes multiple validation steps:

- **Material Completeness**: Ensures all expected file types are present
- **Customization Verification**: Confirms all agent information placeholders are filled
- **Format Validation**: Checks file integrity and accessibility
- **Packaging Verification**: Validates final package structure and contents

## Troubleshooting

### Common Issues

**Missing Materials**
- Ensure builder directory contains all expected file types
- Check file permissions and accessibility

**Website Access Issues**
- Verify builder website URL is accessible
- Check for any authentication requirements

**Customization Failures**
- Review agent information format requirements
- Check for special characters or encoding issues

### Logs and Debugging

- Pipeline execution logs are stored in `artifacts/logs/`
- Validation reports provide detailed error information
- Use visualization template to track progress and identify bottlenecks

## Integration Points

### Builder Systems
- Direct integration with builder material directories
- Web scraping capabilities for builder websites
- Support for common builder file formats and structures

### CRM Integration
- Agent contact information synchronization
- Client communication templates
- Package delivery tracking

### Document Management
- Version control for customized materials
- Audit trails for changes and approvals
- Backup and recovery procedures

## Best Practices

### Material Preparation
- Organize builder materials in clear directory structures
- Use consistent file naming conventions
- Include metadata files when available

### Customization
- Maintain templates for common agent information
- Document customization requirements clearly
- Test customizations with sample data

### Quality Assurance
- Always run validation checks before client delivery
- Maintain backup copies of original materials
- Document any manual customization steps

## Support

For issues or questions:
- Check the [troubleshooting guide](#troubleshooting)
- Review pipeline logs in `artifacts/logs/`
- Contact the development team

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

- **2025-11-16**: Initial pipeline creation
  - Basic condo application package workflow
  - Multi-format material processing
  - Agent customization framework
  - Quality validation system