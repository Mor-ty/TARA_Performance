import os
import datetime

TEMPLATE_PATH = "app/templates/jmx_template.jmx"
OUTPUT_DIR = "app/templates"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"sauce_load_test_{timestamp}.jmx"

ACTIONS = [
    {"name": "Login", "method": "GET", "path": "/", "params": ["username", "password"]},
    {"name": "Search", "method": "GET", "path": "/inventory.html", "params": ["search_keyword"]},
    {"name": "AddToCart", "method": "POST", "path": "/cart.html", "params": ["product_id", "quantity"]},
    {"name": "Checkout", "method": "POST", "path": "/checkout-step-one.html", "params": ["cart_id", "payment_id"]},
]


def read_template(path=TEMPLATE_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_request_block(action):
    params_xml = "\n".join(
        f"""
            <elementProp name="" elementType="HTTPArgument">
                <stringProp name="Argument.value">${{{p}}}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
                <boolProp name="HTTPArgument.use_equals">true</boolProp>
            </elementProp>
        """ for p in action["params"]
    )

    return f"""
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{action['name']}">
          <stringProp name="HTTPSampler.domain">www.saucedemo.com</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.path">{action['path']}</stringProp>
          <stringProp name="HTTPSampler.method">{action['method']}</stringProp>
          <boolProp name="HTTPSampler.postBodyRaw">false</boolProp>

          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" 
                       guiclass="HTTPArgumentsPanel" testclass="Arguments" 
                       testname="User Defined Variables">
            <collectionProp name="Arguments.arguments">
              {params_xml}
            </collectionProp>
          </elementProp>
        </HTTPSamplerProxy>
        <hashTree/>
    """


def generate_request_blocks(actions=ACTIONS):
    return "\n".join(generate_request_block(a) for a in actions)


def generate_jmx_file(concurrent_users, ramp_up, duration,
                      template_path=TEMPLATE_PATH,
                      output_dir=OUTPUT_DIR,
                      output_file=OUTPUT_FILE):

    template_content = read_template(template_path)
    request_blocks = generate_request_blocks()

    jmx_content = (
        template_content
        .replace("${users}", str(concurrent_users))
        .replace("${ramp_up}", str(ramp_up))
        .replace("${duration}", str(duration))
        .replace("${REQUEST_BLOCKS}", request_blocks)
        .replace("${test_name}", "Sauce.com Load Test")
    )

    os.makedirs(output_dir, exist_ok=True)
    jmx_path = os.path.join(output_dir, output_file)

    with open(jmx_path, "w", encoding="utf-8") as f:
        f.write(jmx_content)

    return jmx_path


def main():
    concurrent_users = 100
    ramp_up = 15
    duration = 40
    jmx_file = generate_jmx_file(concurrent_users, ramp_up, duration)
    print(f"Generated JMeter test plan at: {jmx_file}")


if __name__ == "__main__":
    main()
