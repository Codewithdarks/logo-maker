from certificate_generator import CertificateGenerator

# Create certificates with different logo positions matching HTML design
generator = CertificateGenerator()

# Base certificate data matching HTML design exactly
base_data = {
    'course_title': 'Certificate of Completion',
    'course_sub': 'Welcome!',
    'name': 'Sachin Kumar',
    'value': 'has successfully completed WorkTRADE, an online training module on the Prevention of Insider Trading in India covering the Securities and Exchange Board of India (SEBI) Regulations. By completing this training module, you have demonstrated your dedication to upholding ethical standards in the financial markets and preventing the misuse of confidential information. Your commitment to compliance and integrity is commendable.',
    'date': '09-09-2023',
    'ceo_signature': 'https://s3rain.s3.ap-south-1.amazonaws.com/1749188910271_Antony_Alex_RM_Signatory.jpg.png',
    'ceo_name': 'Antony Alex',
    'ceo_title': 'CEO - Rainmaker'
}

# Test 1: Logo on the left (default)
left_data = base_data.copy()
left_data['logo_position'] = 'left'
generator.create_certificate('certificate_logo_left.pdf', left_data)
print("Created certificate with logo on left")

# Test 2: Logo on the right
right_data = base_data.copy()
right_data['logo_position'] = 'right'
generator.create_certificate('certificate_logo_right.pdf', right_data)
print("Created certificate with logo on right")

# Test 3: Logo in center
center_data = base_data.copy()
center_data['logo_position'] = 'center'
generator.create_certificate('certificate_logo_center.pdf', center_data)
print("Created certificate with logo in center")

print("\nAll certificates created successfully!")
print("Certificates saved in the current directory:")
print("- certificate_logo_left.pdf")
print("- certificate_logo_right.pdf") 
print("- certificate_logo_center.pdf")