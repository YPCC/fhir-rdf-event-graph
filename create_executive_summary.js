const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 18 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", quickFormat: true,
        run: { size: 20, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 100, after: 60 }, outlineLevel: 1 } }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 720, right: 720, bottom: 720, left: 720 } // 0.5 inch margins
      }
    },
    children: [
      // Title
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new TextRun({ text: "FHIR-RDF Patient Event Graph POC", bold: true, size: 32, color: "1F4E79" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 160 },
        children: [new TextRun({ text: "Executive Summary | Colorectal Cancer Patient Timeline Visualization", size: 18, italics: true, color: "666666" })]
      }),

      // Problem
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Problem")] }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun("Oncology patient data is fragmented across EHRs, labs, and imaging systems. Clinicians and researchers lack an integrated, visual, standards-based way to explore complete patient journeys — especially for complex cancer cases like colorectal cancer.")]
      }),

      // Solution
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Solution")] }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun("An end-to-end open-source pipeline that converts FHIR patient data into a rich RDF knowledge graph, with native GraphDB visualization, interactive Python timelines, animated GIFs, and mCODE oncology alignment — all deployable in one command via Docker.")]
      }),

      // Key Features
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Key Features")] }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun("• FHIR R4 → RDF (Turtle) conversion with blank node handling  • Interactive GraphDB Visual Graph explorer  • Plotly timelines + high-quality animated patient journey GIFs  • mCODE alignment for oncology  • SHACL validation  • One-click Docker Compose (GraphDB + Streamlit)  • Bulk Synthea processing support")]
      }),

      // Tech Stack
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Technology Stack")] }),
      new Table({
        width: { size: 10800, type: WidthType.DXA },
        columnWidths: [2700, 2700, 2700, 2700],
        rows: [
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "FHIR / Data", bold: true, color: "FFFFFF", size: 16 })] })] }),
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "RDF / Graph", bold: true, color: "FFFFFF", size: 16 })] })] }),
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Visualization", bold: true, color: "FFFFFF", size: 16 })] })] }),
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Deployment", bold: true, color: "FFFFFF", size: 16 })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "HAPI FHIR, Synthea", size: 15 })] })] }),
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "GraphDB Free, rdflib", size: 15 })] })] }),
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Plotly, Matplotlib, Gephi", size: 15 })] })] }),
              new TableCell({ borders, width: { size: 2700, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Docker Compose, Streamlit", size: 15 })] })] })
            ]
          })
        ]
      }),

      // Value
      new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 140 }, children: [new TextRun("Business Value")] }),
      new Paragraph({
        spacing: { after: 80 },
        children: [new TextRun("Delivers a production-ready foundation for oncology data interoperability, clinical decision support, and research. Enables instant visualization of complex cancer patient journeys while maintaining full compliance with HL7 FHIR and mCODE standards.")]
      }),

      // Call to Action
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120 },
        children: [
          new TextRun({ text: "Ready to transform cancer patient data visualization? ", bold: true, size: 18 }),
          new TextRun({ text: "Clone the repo and run with Docker in under 2 minutes.", size: 18, color: "2E75B6" })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 60 },
        children: [new TextRun({ text: "github.com/YOUR_USERNAME/fhir-rdf-event-graph", size: 16, color: "666666" })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/home/workdir/artifacts/fhir-rdf-event-graph/FHIR_RDF_Executive_Summary_OnePage.docx", buffer);
  console.log("One-page executive summary created successfully!");
});