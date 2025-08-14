# certificate_runner.py
# Make sure you have the CertificateGenerator class from the previous file

from certificate_generator import CertificateGenerator

def create_multiple_certificates():
    """Create multiple certificates with different data matching HTML design"""
    
    generator = CertificateGenerator()
    
    # Certificate 1 - Matching HTML design exactly
    certificate_data_1 = {
        'course_title': 'Certificate of Completion',
        'course_sub': 'Welcome!',
        'name': 'Sachin Sagar',
        'value': 'has successfully completed WorkTRADE, an online training module on the Prevention of Insider Trading in India covering the Securities and Exchange Board of India (SEBI) Regulations. By completing this training module, you have demonstrated your dedication to upholding ethical standards in the financial markets and preventing the misuse of confidential information. Your commitment to compliance and integrity is commendable.',
        'date': '09-09-2023',
        'ceo_signature': 'https://s3rain.s3.ap-south-1.amazonaws.com/1749188910271_Antony_Alex_RM_Signatory.jpg.png',
        'ceo_name': 'Antony Alex',
        'ceo_title': 'CEO - Rainmaker'
    }
    
    # Certificate 2 - Custom example
    certificate_data_2 = {
        'course_title': 'Certificate of Completion',
        'course_sub': 'Welcome!',
        'name': 'Alice Johnson',
        'value': 'has successfully completed WorkTRADE, an online training module on the Prevention of Insider Trading in India covering the Securities and Exchange Board of India (SEBI) Regulations. By completing this training module, you have demonstrated your dedication to upholding ethical standards in the financial markets and preventing the misuse of confidential information. Your commitment to compliance and integrity is commendable.',
        'date': '15-08-2024',
        'ceo_signature': 'https://s3rain.s3.ap-south-1.amazonaws.com/1749188910271_Antony_Alex_RM_Signatory.jpg.png',
        'ceo_name': 'Antony Alex',
        'ceo_title': 'CEO - Rainmaker'
    }
    
    # Generate certificates
    generator.create_certificate('sachin_certificate.pdf', certificate_data_1)
    generator.create_certificate('alice_certificate.pdf', certificate_data_2)
    
    print("All certificates generated successfully!")

def create_single_certificate():
    """Create a single certificate matching HTML design"""
    
    generator = CertificateGenerator()
    
    # Get user input
    name = input("Enter recipient name: ") or "John Doe"
    date = input("Enter date (DD-MM-YYYY): ") or "09-09-2023"
    
    certificate_data = {
        'course_title': 'Certificate of Completion',
        'course_sub': 'Welcome!',
        'name': name,
        'value': 'has successfully completed WorkTRADE, an online training module on the Prevention of Insider Trading in India covering the Securities and Exchange Board of India (SEBI) Regulations. By completing this training module, you have demonstrated your dedication to upholding ethical standards in the financial markets and preventing the misuse of confidential information. Your commitment to compliance and integrity is commendable.',
        'date': date,
        'ceo_signature': 'https://s3rain.s3.ap-south-1.amazonaws.com/1749188910271_Antony_Alex_RM_Signatory.jpg.png',
        'ceo_name': 'Antony Alex',
        'ceo_title': 'CEO - Rainmaker'
    }
    
    filename = f"{name.replace(' ', '_').lower()}_certificate.pdf"
    generator.create_certificate(filename, certificate_data)
    print(f"Certificate created: {filename}")

if __name__ == "__main__":
    print("Certificate Generator - HTML Design Match")
    print("1. Create single certificate (interactive)")
    print("2. Create multiple sample certificates")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        create_single_certificate()
    elif choice == "2":
        create_multiple_certificates()
    else:
        print("Invalid choice. Creating sample certificate...")
        create_multiple_certificates()