import streamlit as st
import random
import string
from datetime import datetime, timedelta
from io import BytesIO
import base64
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

# Configure page
st.set_page_config(
    page_title="GCash Cash-In",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-like interface
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default padding and move everything up */
    .main > div {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 400px;
    }
    
    /* Remove default container padding and move up */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 400px;
        padding-top: 0 !important;
    }
    
    /* Move the entire app container up */
    .appview-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Custom styling */
    .gcash-header {
        background: linear-gradient(135deg, #007AFF 0%, #005CE6 100%);
        color: white;
        padding: 15px 20px;
        margin: 0;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 18px;
        font-weight: 600;
        position: relative;
        min-height: 60px;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .back-arrow {
        font-size: 20px;
        cursor: pointer;
    }
    
    .info-icon {
        font-size: 20px;
        width: 24px;
        height: 24px;
        border: 2px solid white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        cursor: pointer;
    }
    
    .content-top-section {
        background: white;
        padding: 30px 20px;
        border-radius: 25px 25px 0 0;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .description-text {
        text-align: center;
        color: #666;
        font-size: 16px;
        line-height: 1.4;
        margin: 0 0 20px 0;
        font-weight: 400;
    }
    
    .amount-section {
        margin: 0 0 20px 0;
    }
    
    .amount-label {
        color: #333;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 15px;
    }
    
    .amount-input-container {
        background: #F8F9FA;
        border-radius: 10px;
        padding: 0;
        box-shadow: none;
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
    }
    
    .stTextInput > div > div > input {
        background: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 20px !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        color: #333 !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .content-bottom-section {
        padding: 20px;
    }
    
    .warning-text {
        text-align: center;
        color: #666;
        font-size: 14px;
        line-height: 1.4;
        margin: 20px 0 30px 0;
        font-weight: 400;
    }
    
    /* Fixed button styling for GENERATE CODE */
    .stButton[data-testid="generate_btn"] > button {
        background: linear-gradient(135deg, #32D9FF 0%, #1AC7FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 18px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(50, 217, 255, 0.3) !important;
        height: auto !important;
        min-height: 55px !important;
    }
    
    .stButton[data-testid="generate_btn"] > button:hover {
        background: linear-gradient(135deg, #1AC7FF 0%, #00B8FF 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(50, 217, 255, 0.4) !important;
    }
    
    .stButton[data-testid="generate_btn"] > button:focus {
        background: linear-gradient(135deg, #32D9FF 0%, #1AC7FF 100%) !important;
        box-shadow: 0 4px 15px rgba(50, 217, 255, 0.3) !important;
    }
    
    .stButton[data-testid="generate_btn"] > button:active {
        background: linear-gradient(135deg, #1AC7FF 0%, #00B8FF 100%) !important;
        transform: translateY(0) !important;
    }
    
    .barcode-instructions {
        text-align: center;
        color: #666;
        font-size: 14px;
        line-height: 1.4;
        margin: 20px 0;
        padding: 0 20px;
    }
    
    .amount-display {
        text-align: center;
        margin: 20px 0;
    }
    
    .amount-display-label {
        color: #666;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .amount-value {
        color: #000;
        font-size: 32px;
        font-weight: 700;
    }
    
    .barcode-container {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .barcode-number { 
        font-family: monospace;
        font-size: 20px; 
        font-weight: 600; 
        margin-top: 10px; 
        word-break: break-all;
        text-align: center;
        color: #333;
        letter-spacing: 2px; 
    }
    
    .reference-code-container {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .reference-code {
        font-family: monospace;
        font-size: 24px;
        font-weight: 600;
        color: #333;
        flex: 1;
        text-align: center;
    }
    
    .copy-icon {
        color: #007AFF;
        font-size: 20px;
        cursor: pointer;
        margin-left: 15px;
    }
    
    .validity-info {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin: 30px 0;
        padding: 0 20px;
    }
    
    .validity-label {
        margin-bottom: 5px;
    }
    
    .validity-date {
        font-weight: 600;
        color: #333;
    }
    
    .gcash-branding {
        text-align: center;
        margin: 40px 0;
    }
    
    
    .gcash-subtitle {
        color: #666;
        font-size: 20px;
        margin: 5px 0;
        font-weight: 400;
    }
    
    /* Fixed button styling for DONE */
    .stButton[data-testid="done_btn"] > button {
        background: linear-gradient(135deg, #32D9FF 0%, #1AC7FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 18px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(50, 217, 255, 0.3) !important;
        height: auto !important;
        min-height: 55px !important;
        margin: 0 20px !important;
    }
    
    .stButton[data-testid="done_btn"] > button:hover {
        background: linear-gradient(135deg, #1AC7FF 0%, #00B8FF 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(50, 217, 255, 0.4) !important;
    }
    
    .stButton[data-testid="done_btn"] > button:focus {
        background: linear-gradient(135deg, #32D9FF 0%, #1AC7FF 100%) !important;
        box-shadow: 0 4px 15px rgba(50, 217, 255, 0.3) !important;
    }
    
    .stButton[data-testid="done_btn"] > button:active {
        background: linear-gradient(135deg, #1AC7FF 0%, #00B8FF 100%) !important;
        transform: translateY(0) !important;
    }
    
    /* Hide back button from display but keep functionality */
    .stButton[data-testid="back_btn"] {
        display: none !important;
    }
    
    /* Hide copy button from display but keep functionality */
    .stButton[data-testid="copy_btn"] {
        display: none !important;
    }
    
    .error-message {
        color: #EF4444;
        font-size: 14px;
        margin-top: 10px;
        padding: 10px;
        background: #FEF2F2;
        border-radius: 8px;
        border-left: 4px solid #EF4444;
    }
    
    .success-message {
        color: #10B981;
        font-size: 14px;
        margin-top: 10px;
        padding: 10px;
        background: #F0FDF4;
        border-radius: 8px;
        border-left: 4px solid #10B981;
    }
    
    /* Remove default Streamlit spacing */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Move everything to the very top */
    .stApp {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove any top margin from the main container */
    .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_barcode_code():
    """Generate a 24-character code with fixed prefix 28101090 and 16 random digits."""
    # Fixed first 8 digits: 28101090
    fixed_prefix = "28101090"
    # 16 random digits for the suffix
    random_suffix = ''.join(random.choices(string.digits, k=16))
    code = fixed_prefix + random_suffix
    return code

def generate_reference_code():
    """Generate an 8-digit reference code"""
    return str(random.randint(10000000, 99999999))

def create_barcode_image(code):
    """Create barcode image using python-barcode"""
    try:
        # Create barcode
        barcode = Code128(code, writer=ImageWriter())
        
        # Generate barcode image
        buffer = BytesIO()
        barcode.write(buffer)
        buffer.seek(0)
        
        # Convert to base64 for display
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return img_base64
    except Exception as e:
        st.error(f"Barcode generation failed: {str(e)}")
        return None

def format_amount(amount):
    """Format amount with proper currency formatting"""
    try:
        num = float(amount)
        return f"{num:,.2f}"
    except:
        return "0.00"

def validate_amount(amount_str):
    """Validate the entered amount"""
    try:
        amount = float(amount_str)
        if amount < 1:
            return False, "Please enter a valid amount between ₱1 and ₱50,000"
        elif amount > 50000:
            return False, "Please enter a valid amount between ₱1 and ₱50,000"
        return True, ""
    except:
        return False, "Please enter a valid amount between ₱1 and ₱50,000"

def main():
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 'input'
    if 'barcode_data' not in st.session_state:
        st.session_state.barcode_data = None
    if 'amount' not in st.session_state:
        st.session_state.amount = ""

    # Header
    st.markdown("""
    <div class="gcash-header">
        <div class="header-left">
            <span class="back-arrow">←</span>
            <span>Cash-In via Code</span>
        </div>
        <div class="info-icon">i</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.step == 'input':
        # Input Step
        st.markdown('<div class="gcash-content">', unsafe_allow_html=True)
        
        # Description
        st.markdown("""
        <div class="description-text">
            Cash In made easier via Barcode or a unique Reference Code
        </div>
        """, unsafe_allow_html=True)
        
        # Amount Input Section
        st.markdown('<div class="amount-section">', unsafe_allow_html=True)
        
        # Amount Label
        st.markdown("""
        <div class="amount-label">PHP</div>
        """, unsafe_allow_html=True)
        
        # Amount Input with custom styling
        st.markdown('<div class="amount-input-container">', unsafe_allow_html=True)
        
        amount_input = st.text_input(
            "",
            value=st.session_state.amount,
            placeholder="500",
            key="amount_input",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Validation and error display
        error_message = ""
        if amount_input:
            is_valid, error_msg = validate_amount(amount_input)
            if not is_valid:
                st.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                error_message = error_msg
            else:
                st.session_state.amount = amount_input
        
        # Warning text
        st.markdown("""
        <div class="warning-text">
            Please check the amount before you proceed.
        </div>
        """, unsafe_allow_html=True)
        
        # Generate button
        if st.button("GENERATE CODE", key="generate_btn", use_container_width=True):
            if amount_input and not error_message:
                is_valid, error_msg = validate_amount(amount_input)
                if is_valid:
                    # Generate barcode data
                    barcode_code = generate_barcode_code()
                    reference_code = generate_reference_code()
                    expiry_date = datetime.now() + timedelta(hours=24)
                    
                    st.session_state.barcode_data = {
                        'code': barcode_code,
                        'reference_code': reference_code,
                        'expiry_date': expiry_date.strftime("%d %B %Y %I:%M:%S %p"),
                        'amount': amount_input
                    }
                    st.session_state.step = 'barcode'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # End gcash-content
    
    else:
        # Barcode Display Step
        st.markdown('<div class="gcash-content">', unsafe_allow_html=True)
        
        # Back button (hidden but functional)
        if st.button("← Back", key="back_btn"):
            st.session_state.step = 'input'
            st.rerun()
        
        # Instructions
        st.markdown("""
        <div class="barcode-instructions">
            Show one of these codes to the cashier of any participating merchant to Cash In.
        </div>
        """, unsafe_allow_html=True)
        
        # Amount display
        if st.session_state.barcode_data:
            amount = st.session_state.barcode_data['amount']
            st.markdown(f"""
            <div class="amount-display">
                <div class="amount-display-label">the amount of</div>
                <div class="amount-value">php {format_amount(amount)}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate and display barcode
            barcode_img = create_barcode_image(st.session_state.barcode_data['code'])
            if barcode_img:
                st.markdown("""
                <div class="barcode-container">
                """, unsafe_allow_html=True)
                
                # Display barcode image
                st.markdown(f"""
                <img src="data:image/png;base64,{barcode_img}" style="max-width: 100%; height: auto;">
                <div class="barcode-number">
                    {st.session_state.barcode_data['code']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Reference code with copy functionality
            st.markdown(f"""
            <div class="reference-code-container">
                <div class="reference-code">{st.session_state.barcode_data['reference_code']}</div>
                <div class="copy-icon">📋</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Copy button functionality (hidden but functional)
            copy_clicked = st.button("Copy", key="copy_btn")
            
            if copy_clicked:
                st.markdown("""
                <div class="success-message">
                    Reference code copied to clipboard! (Note: Manual copy required in this demo)
                </div>
                """, unsafe_allow_html=True)
            
            # Validity information
            st.markdown(f"""
            <div class="validity-info">
                <div class="validity-label">valid until</div>
                <div class="validity-date">{st.session_state.barcode_data['expiry_date']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # GCash branding
            st.markdown("""
            <div class="gcash-branding">
                <div class="gcash-logo">Cash In</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Done button
            if st.button("DONE", key="done_btn", use_container_width=True):
                st.session_state.step = 'input'
                st.session_state.amount = ""
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()