import subprocess
import os

JMETER_PATH = os.path.join("C:\\Users\\rahulde\\Downloads\\apache-jmeter-5.6.3\\apache-jmeter-5.6.3", "bin", "jmeter.bat")

def run_jmeter(jmx_path):
    results_file = "results/results.jtl"
    report_dir = "results/html_report"

    os.makedirs("results", exist_ok=True)

    cmd = [
        JMETER_PATH,
        "-n",
        "-t", jmx_path,
        "-l", results_file,
        "-e",
        "-o", report_dir
    ]

    print("Running JMeter...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = proc.communicate()

    print("\n--- JMeter Output ---\n")
    print(out.decode())
    print("\n--- JMeter Errors ---\n")
    print(err.decode())

    print("\nHTML Report generated at:", report_dir)
    return results_file, report_dir


if __name__ == "__main__":
    jmx_file = "C:\\Users\\rahulde\\Documents\\performance_TARA\\app\\templates\\sauce_load_test_20251117_145107.jmx"
    run_jmeter(jmx_file)
