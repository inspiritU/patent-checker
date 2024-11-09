import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os
from datetime import datetime


def create_app():
    app = Flask(__name__)
    CORS(app)  # 启用跨域支持

    # 加载数据文件
    base_dir = os.path.dirname(os.path.abspath(__file__))
    patents_path = os.path.join(base_dir, 'patents.json')
    company_products_path = os.path.join(base_dir, 'company_products.json')

    try:
        with open(patents_path) as f:
            patents_data = json.load(f)

        with open(company_products_path) as f:
            company_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        patents_data = []
        company_data = {"companies": []}

    # 初始化 OpenAI 客户端
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("Warning: OpenAI API key not set.")

    # 首页路由
    @app.route('/')
    def index():
        return "Welcome to the Patent Checker API!"

    # 使用 LLM 分析侵权
    def analyze_infringement(claims: str, product_description: str):
        messages = [
            {
                "role": "system",
                "content": "You are a patent infringement analysis assistant. Respond strictly in JSON format as specified below."
            },
            {
                "role": "user",
                "content": (
                    f"Patent Claims: {claims}\n"
                    f"Product Description: {product_description}\n"
                    "Provide the analysis in the following JSON format:\n\n"
                    "{\n"
                    "  \"likelihood\": \"High, Moderate, or Low\",\n"
                    "  \"relevant_claims\": [\"List\", \"of\", \"claim\", \"numbers\"],\n"
                    "  \"explanation\": \"A brief explanation of the analysis\",\n"
                    "  \"specific_features\": [\n"
                    "    \"Feature 1 description\",\n"
                    "    \"Feature 2 description\",\n"
                    "    \"Feature 3 description\"\n"
                    "  ]\n"
                    "}\n\n"
                    "Please ensure that the number of items in \"specific_features\" is equal to the number of items in \"relevant_claims\". "
                    "Provide only the JSON object as the response, no additional text."
                ),
            },
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7,
            )
            result_text = response['choices'][0]['message']['content'].strip()
            print('LLM Response:', result_text)

            result_json = json.loads(result_text)
        except (openai.error.OpenAIError, json.JSONDecodeError) as e:
            print(f"Error during OpenAI interaction: {e}")
            return {
                "likelihood": "Unknown",
                "relevant_claims": [],
                "explanation": "Failed to analyze using OpenAI.",
                "specific_features": []
            }

        return {
            "likelihood": result_json.get("likelihood", "Low"),
            "relevant_claims": [str(claim) for claim in result_json.get("relevant_claims", [])],
            "explanation": result_json.get("explanation", ""),
            "specific_features": result_json.get("specific_features", [])
        }

    # 专利侵权检查路由
    @app.route('/check_infringement', methods=['POST', 'OPTIONS'])
    def check():
        if request.method == 'OPTIONS':
            # 允许浏览器跨域预检请求
            return '', 200

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid data"}), 400

        patent_id = data.get('patent_id')
        company_name = data.get('company_name')

        if not patent_id or not company_name:
            return jsonify({"message": "Missing patent_id or company_name"}), 400

        # 检查专利侵权
        result = check_infringement(patent_id, company_name)
        if not result:
            return jsonify({"message": "No infringing products found"}), 404

        return jsonify(result)

    def check_infringement(patent_id, company_name):
        print(f"Checking infringement for patent_id={patent_id}, company_name={company_name}")

        # 从数据中获取专利和公司信息
        patent = next((p for p in patents_data if p['publication_number'] == patent_id), None)
        company = next((c for c in company_data['companies'] if c['name'].lower() == company_name.lower()), None)

        if not patent or not company:
            print("No matching patent or company found.")
            return None

        infringing_products = []
        for product in company['products']:
            analysis = analyze_infringement(
                claims=patent['claims'],
                product_description=product['description']
            )

            # 添加侵权分析结果
            infringing_products.append({
                "product_name": product['name'],
                "infringement_likelihood": analysis['likelihood'],
                "relevant_claims": analysis['relevant_claims'],
                "explanation": analysis['explanation'],
                "specific_features": analysis['specific_features']
            })

        # 排序逻辑保持动态计算
        likelihood_priority = {"High": 3, "Moderate": 2, "Low": 1}
        sorted_products = sorted(
            infringing_products,
            key=lambda x: (
                likelihood_priority.get(x["infringement_likelihood"], 0),
                len(x["relevant_claims"])  # 动态计算 claims_count
            ),
            reverse=True
        )

        # 返回高风险的前两个产品
        top_infringing_products = sorted_products[:2] if len(sorted_products) >= 2 else sorted_products

        # 动态生成 overall_risk_assessment
        main_product = top_infringing_products[0] if top_infringing_products else None
        additional_product = top_infringing_products[1] if len(top_infringing_products) > 1 else None

        if main_product:
            overall_risk_assessment = (
                f"High risk of infringement due to implementation of core patent claims in {main_product['product_name']}, "
                f"which implements most key elements of the patent claims."
            )
            if additional_product:
                additional_risk = "moderate" if additional_product["infringement_likelihood"] == "Moderate" else "high"
                overall_risk_assessment += (
                    f" {additional_product['product_name']} presents additional {additional_risk} risk through its "
                    "partial implementation of the patented technology."
                )
        else:
            overall_risk_assessment = "No significant risk of infringement detected."

        return {
            "analysis_id": "1",
            "patent_id": patent_id,
            "company_name": company_name,
            "analysis_date": datetime.today().strftime('%Y-%m-%d'),
            "top_infringing_products": top_infringing_products,
            "overall_risk_assessment": overall_risk_assessment
        }

    return app