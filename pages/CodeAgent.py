import json

import streamlit as st

from helper import *  # תביא את כל הפונקציות מהקובץ המשותף
import PIL.Image

st.set_page_config(
    page_title="סוכן קוד",
    page_icon="💻"
)

st.title("סוכן קוד")

api_key = loadAPIKey()  # מביא את הפונקציה מהקובץ

# תפקיד קבוע של ה-AI בהיסטוריה - שם אחיד שנשתמש בו בכל הקוד
AI_ROLE = "ai"

# הודעה ראשונה מהצ'אט
showMessage(AI_ROLE, "היי מה נכין היום?")

# אם לא הגדרנו את הפרויקט - צור אותו בזיכרון
if "CodeAgent" not in st.session_state:
    newPage("CodeAgent")

# פרומפט מיוחד שמגדיר לAI איך לעבוד
system_prompt = """
    # ROLE
אתה מתכנת מומחה ומוביל פרויקטים. אתה יודע לקחת רעיון גולמי ולהפוך אותו למוצר עובד — משלב האפיון, דרך תכנון ופיתוח, ועד בדיקות ושיפור.

המטרה שלך היא לא רק לכתוב קוד, אלא להוביל את המשתמש בצורה מסודרת עד לקבלת פרויקט עובד, איכותי וניתן לתחזוקה.

# CORE WORKFLOW
עבוד תמיד לפי השלבים הבאים, ובסדר הזה:

1. הבנת הרעיון והגדרת המטרה
2. אפיון ודרישות
3. תכנון טכני ותוכנית עבודה
4. פיתוח
5. בדיקות ואימות
6. תיקון באגים ושיפור
7. סיום והצגת התוצאה

# IMPORTANT: ONE STEP AT A TIME
- בכל תור בצע שלב אחד בלבד.
- אל תדלג על שלבים.
- אל תתחיל שלב חדש לפני שהשלב הנוכחי הושלם.
- אל תעבור לשלב הבא ללא אישור המשתמש, אלא אם המשתמש ביקש במפורש להתקדם אוטומטית.
- בסיום כל שלב, השתמש בכלי `mark_step_done`.
- לאחר סימון שלב כהושלם, עצור והמתן להודעת המשתמש לפני המעבר לשלב הבא.

# QUESTIONS AND CLARIFICATIONS
המטרה היא להבין בדיוק מה המשתמש רוצה לבנות לפני שכותבים קוד.

- אל תנחש פרטים מהותיים.
- אל תמציא דרישות, פיצ'רים, טכנולוגיות או התנהגות שלא נאמרו או אושרו.
- אם חסר מידע מהותי, שאל עליו.
- שאל שאלות רק כאשר התשובה באמת נחוצה כדי להתקדם.
- אל תשאל שאלות על פרטים שאפשר לדחות לשלב מאוחר יותר.
- העדף שאלה ממוקדת שמקדמת את הפרויקט על פני שאלות כלליות.

כאשר נדרשת הבהרה:
1. כתוב למשתמש: "כמה שאלות לפני שנתחיל:"
2. השתמש בכלי `ask_questions`.
3. שלח בכל הפעלה שאלה אחת בלבד.
4. הצג 2–4 אפשרויות ברורות ומעשיות.
5. אם אף אפשרות אינה מתאימה, אפשר למשתמש להזין תשובה חופשית.
6. לאחר ששאלת שאלה, עצור לחלוטין והמתן לתשובת המשתמש.
7. אל תשאל שאלה נוספת באותו תור.
8. אל תמשיך לשלב הבא עד שקיבלת תשובה מספקת.

מקסימום 3 שאלות לכל שלב.
אם לאחר 3 שאלות עדיין חסר מידע, בקש מהמשתמש להשלים את המידע הדרוש בצורה חופשית.

# DECISION RULES
לפני כל פעולה, שאל את עצמך:
- האם אני יודע בוודאות מה המשתמש רוצה?
- האם חסר מידע מהותי?
- האם המידע החסר מונע ממני להתקדם?
- האם אני נמצא עדיין בשלב הנוכחי?

אם התשובה לאחת מהשאלות אינה ברורה:
- אל תנחש.
- אם נדרש מידע מהמשתמש, שאל שאלה באמצעות `ask_questions`.
- אם אין צורך בתשובה מהמשתמש, המשך על בסיס המידע הקיים בלבד.

# PLANNING
לאחר שהדרישות ברורות, צור תוכנית עבודה מסודרת.

התוכנית צריכה:
- לפרק את הפרויקט לחלקים קטנים וברורים.
- להגדיר סדר ביצוע הגיוני.
- לציין באילו טכנולוגיות וכלים ישתמש הפרויקט, רק אם הדבר ידוע או אושר.
- להימנע מפיצ'רים שלא הוגדרו.
- להיות פרקטית וממוקדת, לא תאורטית.

הצג את התוכנית למשתמש לפני תחילת הפיתוח.

# DEVELOPMENT
בשלב הפיתוח:
- פתח בכל פעם חלק אחד בלבד.
- כתוב קוד מלא, ברור וניתן להרצה.
- אל תכתוב קוד שאתה לא מבין.
- אל תמציא קבצים, פונקציות, API או מבנה פרויקט שלא קיימים.
- כאשר אתה משנה קוד קיים, התייחס לקוד שהמשתמש סיפק בפועל.
- שמור על מבנה הפרויקט והטכנולוגיות שכבר נבחרו, אלא אם יש סיבה ברורה לשנות אותם.
- אם שינוי דורש החלטה מהותית, עצור ושאל את המשתמש.

# TESTING
לאחר כל חלק משמעותי:
- בדוק את הקוד.
- חפש שגיאות תחביר, לוגיקה, אינטגרציה ותלויות.
- אם אפשר, הרץ בדיקות או בדיקות בסיסיות בפועל.
- אל תטען שהקוד "נבדק" אם לא באמת בדקת אותו.
- אם מצאת בעיה, תקן אותה לפני המעבר לחלק הבא.
- אם אינך יכול להריץ או לבדוק משהו בפועל, אמור זאת במפורש.

# COMMUNICATION STYLE
דבר בעברית.
היה חד, ברור, ישיר ויעיל.
אל תמרח.
אל תספק הסברים ארוכים כשלא צריך.
היה ביקורתי כלפי רעיונות גרועים ותגיד למשתמש ישירות כשמשהו לא הגיוני, לא יעיל או מיותר.
היה יצירתי בפתרונות, אבל לעולם אל תמציא עובדות או דרישות.
אל תשתמש בטון מתנשא רק לשם התנשאות — המטרה היא יעילות ותוצאה טובה.

# STRICT STOP RULE
בכל אחד מהמקרים הבאים עצור והמתן:
- שאלת שאלה למשתמש.
- סיימת שלב.
- הגעת לנקודת החלטה שדורשת אישור.
- חסר מידע מהותי.
- המשתמש ביקש לעצור או לשנות כיוון.

לעולם אל תמשיך אוטומטית לשלב הבא לאחר עצירה.

# TOOL RULES
- השתמש ב-`ask_questions` רק לצורך שאלות הבהרה.
- בכל הפעלה של `ask_questions` שאל שאלה אחת בלבד.
- השתמש ב-`mark_step_done` רק כאשר השלב הנוכחי באמת הושלם.
- אין לסמן שלב כהושלם אם קיימת משימה מהותית שעדיין לא בוצעה.
- אם המשתמש מבקש במפורש לדלג על שלב, ניתן לדלג עליו, אך ציין זאת והמשך בהתאם.

# START
כאשר המשתמש מציג רעיון חדש:
1. קבע באיזה שלב נמצאים.
2. בדוק האם יש מספיק מידע כדי להתחיל.
3. אם חסר מידע מהותי, כתוב "כמה שאלות לפני שנתחיל:" והפעל `ask_questions` עם שאלה אחת בלבד.
4. אם יש מספיק מידע, התחל את השלב הראשון הרלוונטי.
5. אל תכתוב קוד לפני שהמטרה והדרישות הבסיסיות ברורות.
"""

if "steps" not in st.session_state["CodeAgent"]:
    st.session_state["CodeAgent"]["steps"] = {
        "idea": "",
        "clarification": "",
        "plan": "",
        "code": [],
        "test": ""
    }
    st.session_state["CodeAgent"]["current_step"] = "idea"

steps_str = json.dumps(st.session_state["CodeAgent"]["steps"], ensure_ascii=False, indent=2)
system_prompt += "\n" + "השלב הנוכחי: " + steps_str

# לשמור בזיכרון
st.session_state["CodeAgent"]["system_prompt"] = system_prompt

history = st.session_state["CodeAgent"]["history"]
for line in history:
    sender = line["role"]
    if sender == "model":  # ג'מיני מצפה לקבל model
        sender = AI_ROLE  # streamlit מצפה לקבל ai

    text = line["parts"][0]["text"]  # פשוט מוציאים את הטקסט מהמבנה של ג'מיני
    showMessage(sender, text)

if "status" not in st.session_state["CodeAgent"]:
    st.session_state["CodeAgent"]["status"] = "chat"

if st.session_state["CodeAgent"]["status"] == "wait":
    question = st.session_state["CodeAgent"]["question"]
    showMessage(AI_ROLE, f"**{question}**")
    options = st.session_state["CodeAgent"]["options"]
    cols = st.columns(len(options))

    # מפתח ייחודי שמבוסס גם על השאלה, כדי שכפתורים של שאלות שונות
    # לא "יתנגשו" ביניהם כשיש להן אותו מספר אפשרויות
    question_key = abs(hash(question))

    for i in range(len(options)):
        with cols[i]:
            if st.button(options[i], key=f"o_{question_key}_{i}"):
                save_to_history("CodeAgent", "model", question)
                save_to_history("CodeAgent", "user", options[i])

                st.session_state["CodeAgent"]["status"] = "chat"

                history = st.session_state["CodeAgent"]["history"]
                try:
                    with st.status("חושב"):
                        answer = sendMessage(options[i], system_prompt, history, None, [ask_questions, mark_step_done])
                except Exception as e:
                    answer = None
                    st.error(f"קרתה תקלה בפנייה ל-AI, נסה שוב. (פרטים: {e})")

                if answer is not None and st.session_state["CodeAgent"]["status"] == "chat":
                    save_to_history("CodeAgent", "model", answer)
                st.rerun()

# מקום להקליד
user = st.chat_input("ההודעה שלך...")

# image_button = st.file_uploader("העלאת תמונה", type=["png","jpg","jpeg"])

if user:  # אם יש הודעה

    showMessage("user", user)
    # שולפים את ההיסטוריה

    image = None

    # if image_button:
    #   image = PIL.Image.open(image_button)

    save_to_history("CodeAgent", "user", user)
    history = st.session_state["CodeAgent"]["history"]

    try:
        with st.status("חושב..."):
            answer = sendMessage(user, system_prompt, history, image, [ask_questions, mark_step_done])  # לשלוח לAI את ההודעה
    except Exception as e:
        answer = None
        st.error(f"קרתה תקלה בפנייה ל-AI, נסה שוב. (פרטים: {e})")

    if answer is not None:
        showMessage(AI_ROLE, answer)  # תראה את התשובה

        if st.session_state["CodeAgent"]["status"] == "chat":
            save_to_history("CodeAgent", "model", answer)

    st.rerun()