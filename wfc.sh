
cd "$(dirname "$0")"

# python src/rule_generator.py src/input.json

python src/multishot_wfc.py src/multishot_wfc.lp src/simple_rules.lp
