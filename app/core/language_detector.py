"""
Language detection utility for multilingual responses.
"""
import re
from typing import Optional


class LanguageDetector:
    """Simple language detector based on text patterns."""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language from text content.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Language code (vi, en, etc.) or 'en' as default
        """
        if not text or not text.strip():
            return 'en'
        
        text = text.lower().strip()
        
        # Vietnamese patterns
        vietnamese_patterns = [
            r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',
            r'\b(tôi|bạn|của|với|trong|này|đó|là|có|không|được|sẽ|đã|và|hoặc|nhưng|nếu|khi|để|cho|về|từ|theo|như|sau|trước|giữa|ngoài|bên|trên|dưới|qua|vào|ra|lên|xuống|tại|ở|gần|xa|nhiều|ít|lớn|nhỏ|tốt|xấu|mới|cũ|nhanh|chậm|cao|thấp|dài|ngắn|rộng|hẹp|sáng|tối|nóng|lạnh|khô|ướt|sạch|bẩn|đúng|sai|dễ|khó|quan|trọng|cần|thiết|phải|nên|muốn|thích|yêu|ghét|biết|hiểu|học|dạy|làm|việc|đi|đến|về|nhà|trường|công|ty|bệnh|viện|chợ|siêu|thị|nhà|hàng|khách|sạn|sân|bay|ga|tàu|bến|xe|đường|phố|thành|phố|tỉnh|huyện|xã|thôn|làng|nước|việt|nam|hà|nội|hồ|chí|minh|đà|nẵng|hải|phòng|cần|thơ|huế|nha|trang|vũng|tàu|buôn|ma|thuột|pleiku|quy|nhơn|thái|nguyên|nam|định|hải|dương|bắc|ninh|hưng|yên|thái|bình|hà|nam|ninh|bình|thanh|hóa|nghệ|an|hà|tĩnh|quảng|bình|quảng|trị|thừa|thiên|huế|quảng|nam|quảng|ngãi|bình|định|phú|yên|khánh|hòa|ninh|thuận|bình|thuận|tây|ninh|bình|dương|đồng|nai|bà|rịa|vũng|tàu|long|an|tiền|giang|bến|tre|trà|vinh|vĩnh|long|đồng|tháp|an|giang|kiên|giang|cà|mau|bạc|liêu|sóc|trăng|hậu|giang|cần|thơ)\b'
        ]
        
        # Check Vietnamese
        for pattern in vietnamese_patterns:
            if re.search(pattern, text):
                return 'vi'
        
        # English patterns (common words)
        english_patterns = [
            r'\b(the|and|or|but|if|when|to|for|of|in|on|at|by|with|from|up|about|into|through|during|before|after|above|below|between|among|under|over|across|around|near|far|here|there|where|what|who|which|how|why|yes|no|not|can|could|should|would|will|shall|may|might|must|have|has|had|do|does|did|is|are|was|were|been|being|get|got|make|made|take|took|come|came|go|went|see|saw|know|knew|think|thought|say|said|tell|told|give|gave|find|found|use|used|work|worked|call|called|try|tried|ask|asked|need|needed|feel|felt|become|became|leave|left|put|put|mean|meant|keep|kept|let|let|begin|began|seem|seemed|help|helped|talk|talked|turn|turned|start|started|show|showed|hear|heard|play|played|run|ran|move|moved|live|lived|believe|believed|hold|held|bring|brought|happen|happened|write|wrote|provide|provided|sit|sat|stand|stood|lose|lost|pay|paid|meet|met|include|included|continue|continued|set|set|learn|learned|change|changed|lead|led|understand|understood|watch|watched|follow|followed|stop|stopped|create|created|speak|spoke|read|read|allow|allowed|add|added|spend|spent|grow|grew|open|opened|walk|walked|win|won|offer|offered|remember|remembered|love|loved|consider|considered|appear|appeared|buy|bought|wait|waited|serve|served|die|died|send|sent|expect|expected|build|built|stay|stayed|fall|fell|cut|cut|reach|reached|kill|killed|remain|remained|suggest|suggested|raise|raised|pass|passed|sell|sold|require|required|report|reported|decide|decided|pull|pulled)\b'
        ]
        
        # Check English
        for pattern in english_patterns:
            if re.search(pattern, text):
                return 'en'
        
        # Default to English if no clear pattern
        return 'en'
    
    @staticmethod
    def get_language_instruction(language: str) -> str:
        """
        Get language instruction for AI models.
        
        Args:
            language: Language code
            
        Returns:
            Instruction text for the model
        """
        instructions = {
            'vi': 'Hãy trả lời bằng tiếng Việt.',
            'en': 'Please respond in English.',
            'zh': '请用中文回答。',
            'ja': '日本語で回答してください。',
            'ko': '한국어로 답변해 주세요.',
            'fr': 'Veuillez répondre en français.',
            'de': 'Bitte antworten Sie auf Deutsch.',
            'es': 'Por favor responda en español.',
            'it': 'Si prega di rispondere in italiano.',
            'pt': 'Por favor, responda em português.',
            'ru': 'Пожалуйста, отвечайте на русском языке.',
            'ar': 'يرجى الرد باللغة العربية.',
            'hi': 'कृपया हिंदी में उत्तर दें।',
            'th': 'กรุณาตอบเป็นภาษาไทย',
            'id': 'Silakan jawab dalam bahasa Indonesia.',
            'ms': 'Sila jawab dalam bahasa Melayu.',
        }
        
        return instructions.get(language, instructions['en'])