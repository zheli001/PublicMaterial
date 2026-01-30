# Condo Application Package Pipeline Execution Guide

## Overview
This guide explains how to execute the condo application package creation pipeline using the provided templates.

## Prerequisites

1. **Builder Materials Directory**: A directory containing all builder-provided materials
   ```
   builder_materials/
   ├── project_brochure.pdf
   ├── floor_plans.pdf
   ├── application_form.pdf
   ├── videos/
   │   ├── project_tour.mp4
   │   └── amenities.mp4
   ├── images/
   │   ├── exterior/
   │   ├── interior/
   │   └── amenities/
   └── documents/
       ├── price_list.pdf
       └── terms_conditions.pdf
   ```

2. **Builder Website Access**: Valid URL to the project's webpage

3. **Agent Information**: Contact details and branding requirements

## Execution Steps

### Step 1: Prepare Configuration
```bash
# Copy the sample configuration
cp config_sample.yaml my_project_config.yaml

# Edit with your specific project details
# Update builder name, website URL, agent info, etc.
```

### Step 2: Set Up Materials
```bash
# Create materials directory structure
mkdir -p builder_materials/{pdfs,videos,images,forms}

# Place builder files in appropriate directories
# - PDFs go in pdfs/
# - Videos go in videos/
# - Images go in images/
# - Forms go in forms/
```

### Step 3: Configure Pipeline
```bash
# Update pipeline_template.yaml with your configuration
# Set the materials directory path and website URL
vim pipeline_template.yaml
```

### Step 4: Execute Pipeline
```bash
# Method 1: Using pipeline executor (if available)
./pipeline_executor.sh pipeline_template.yaml

# Method 2: Manual execution (follow visualization steps)
# Follow the pipeline_visualization_template.md phases manually
```

### Step 5: Review Results
```bash
# Check artifacts directory for outputs
ls -la artifacts/

# Review validation reports
cat artifacts/validation_report.txt

# Check final package
ls -la artifacts/client_ready_package/
```

## Expected Outputs

After successful execution, you should have:

```
artifacts/
├── processed_materials/
│   ├── customized_pdfs/
│   ├── optimized_images/
│   └── customized_forms/
├── validation_reports/
│   ├── completeness_check.txt
│   └── customization_highlights.pdf
├── client_ready_package/
│   ├── README_for_client.md
│   ├── application_package.zip
│   └── distribution_manifest.txt
└── logs/
    └── pipeline_execution.log
```

## Troubleshooting

### Common Issues

**Pipeline Fails to Start**
- Check that all required directories exist
- Verify file permissions on materials directory
- Ensure builder website is accessible

**Material Processing Errors**
- Check file formats are supported
- Verify files are not corrupted
- Ensure sufficient disk space

**Customization Issues**
- Review agent information format
- Check for special characters in branding
- Verify template compatibility

### Logs and Debugging

All pipeline execution is logged to:
- `artifacts/logs/pipeline_execution.log`
- `artifacts/logs/unit_execution_logs/`

For detailed debugging:
1. Check unit-specific logs
2. Review validation reports
3. Use visualization template to identify failed steps

## Performance Notes

- **Parallel Processing**: Phase 1 units can run concurrently for faster execution
- **Large Files**: Video processing may take significant time
- **Network Dependent**: Website analysis requires stable internet connection

## Quality Assurance

Before delivering to clients:
1. ✅ Review customization highlights
2. ✅ Test all links and forms
3. ✅ Verify agent contact information
4. ✅ Check file integrity
5. ✅ Validate package structure

## Support

If you encounter issues:
1. Check this guide and troubleshooting section
2. Review pipeline logs for error details
3. Contact the development team with log excerpts