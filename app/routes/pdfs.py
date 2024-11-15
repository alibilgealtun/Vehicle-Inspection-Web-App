from flask import render_template, send_file, Blueprint, abort
from weasyprint import HTML
from ..models import Report
from ..services.pdf_service import *
pdfs = Blueprint('pdfs', __name__, url_prefix='/pdfs')

@pdfs.route('generate/<int:report_id>')
def generate_report_pdf(report_id):

    try:
        pdf_path = create_pdf(report_id)
    except Exception as e:
        # Eğer PDF oluşturulurken bir hata oluşursa, bunu loglayabilir ve bir hata mesajı döndürebilirsin
        print(f"PDF oluşturulurken bir hata oluştu: {str(e)}")
        abort(500, description="PDF oluşturulamadı.")

    return send_file(pdf_path, mimetype='application/pdf')
