from certificate_generator import CertificateGenerator

# Create a test certificate with sample data matching HTML design exactly
generator = CertificateGenerator()

certificate_data = {
    'logo_position': 'left',
    'course_title': 'Certificate of Completion',
    'course_sub': 'Welcome!',
    'name': 'Sachin Kumar',
    'value': 'has successfully completed WorkTRADE, an online training module on the Prevention of Insider Trading in India covering the Securities and Exchange Board of India (SEBI) Regulations. By completing this training module, you have demonstrated your dedication to upholding ethical standards in the financial markets and preventing the misuse of confidential information. Your commitment to compliance and integrity is commendable.',
    'date': '09-09-2023',
    'ceo_signature': 'https://s3rain.s3.ap-south-1.amazonaws.com/1749188910271_Antony_Alex_RM_Signatory.jpg.png',
    'ceo_name': 'Antony Alex',
    'ceo_title': 'CEO - Rainmaker'
}

generator.create_certificate('sachin_certificate.pdf', certificate_data)
print("Test certificate created successfully!")
print("Certificate saved as: sachin_certificate.pdf in the current directory")