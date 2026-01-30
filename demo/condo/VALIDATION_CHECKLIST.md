# Condo Application Package Pipeline Validation Checklist

## Pre-Execution Checklist

### ✅ Builder Materials Directory
- [ ] Directory exists and is accessible
- [ ] Contains PDF documents (brochures, floor plans, etc.)
- [ ] Contains image files (exterior, interior, amenities)
- [ ] Contains application forms
- [ ] Contains video files (optional but recommended)
- [ ] Files are not corrupted and can be opened
- [ ] Sufficient disk space for processing (2x original size minimum)

### ✅ Builder Website Access
- [ ] Website URL is valid and accessible
- [ ] No authentication requirements
- [ ] Website contains project information
- [ ] Downloadable materials are available (optional)

### ✅ Agent Information
- [ ] Agent name and contact details provided
- [ ] Phone number and email address
- [ ] Brokerage information
- [ ] Branding requirements specified (logo, colors, etc.)
- [ ] All required customization fields identified

### ✅ Pipeline Configuration
- [ ] `pipeline_template.yaml` exists and is valid YAML
- [ ] Project ID and builder information configured
- [ ] Material directory paths are correct
- [ ] Website URL is properly set
- [ ] Agent information is complete
- [ ] Output directory paths are valid

### ✅ System Requirements
- [ ] Sufficient RAM for processing (4GB minimum)
- [ ] Pipeline executor is available
- [ ] Required dependencies installed
- [ ] Network connectivity for website access
- [ ] Write permissions for output directories

## Execution Validation

### Phase 0: Material Collection & Analysis
- [ ] Builder materials successfully inventoried
- [ ] Material types correctly identified
- [ ] Website analysis completed
- [ ] Project information extracted
- [ ] Customization requirements identified
- [ ] Agent placeholders mapped

### Phase 1: Material Processing & Customization
- [ ] PDF documents processed and customized
- [ ] Agent information inserted correctly
- [ ] Customization highlights generated
- [ ] Video content organized
- [ ] Image assets optimized
- [ ] Application forms customized
- [ ] Completion guides created

### Phase 2: Package Assembly & Validation
- [ ] All materials assembled into package
- [ ] Package manifest created
- [ ] Completeness validation passed
- [ ] All required customizations verified
- [ ] Client-ready package prepared
- [ ] Distribution README created

## Post-Execution Quality Checks

### Package Completeness
- [ ] All original materials included
- [ ] All customizations applied
- [ ] No placeholder text remaining
- [ ] File formats preserved
- [ ] File integrity verified

### Customization Quality
- [ ] Agent contact information correct
- [ ] Branding applied consistently
- [ ] Highlighting is clear and professional
- [ ] Forms are fillable and functional

### Client Readiness
- [ ] Package structure is logical
- [ ] File names are professional
- [ ] README instructions are clear
- [ ] Contact information is current
- [ ] All links and references work

## Final Delivery Checklist

### Before Client Delivery
- [ ] Final validation report reviewed
- [ ] Sample files spot-checked
- [ ] Agent approval obtained
- [ ] Backup copy archived
- [ ] Delivery method confirmed

### Delivery Confirmation
- [ ] Package successfully delivered
- [ ] Client acknowledges receipt
- [ ] Follow-up instructions provided
- [ ] Support contact information given

## Issue Resolution

If any checklist item fails:

1. **Document the issue** with specific details
2. **Check logs** in `artifacts/logs/` directory
3. **Review configuration** for errors
4. **Verify input materials** for problems
5. **Contact support** with issue details and logs

## Success Criteria

Pipeline execution is successful when:
- ✅ All pre-execution checklist items pass
- ✅ All execution validation steps complete
- ✅ All quality checks pass
- ✅ Client-ready package is generated
- ✅ No critical errors in logs
- ✅ Validation report shows 100% completeness

---

*Validation performed on: [Date]*
*Validated by: [Name]*
*Pipeline Version: 1.0.0*