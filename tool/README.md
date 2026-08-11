# FSF-Slicer-TBFV

这是论文 **FSF-Guided Program Slicing for Testing-Based Formal Verification of Functional Soundness and Completeness** 的独立可运行复现。工具以 Java 源文件和 Functional Scenario Form（FSF）为输入，生成每个场景对应的可执行 Java 切片，并按照论文的 TBFV 流程判断 functional soundness 与 functional completeness。

本项目默认完全离线：Java 解析、PDG、切片、测试生成、符号路径推导和 Z3 验证均在本地完成。LLM 只用于可选的 `suggest-fsf` 草拟命令；它不会参与最终形式化判定，也不会保存 API key。

## 已实现能力

- Java 方法解析、方法/参数/返回类型核验。
- FSF YAML 解析与严格预检：变量约束、`T` 可满足性、`T` 互斥性、场景族输入覆盖、`D` 输出约束与重叠提示。
- 控制流/程序依赖图的保守构建：参数、DEF/USE、数据依赖、控制依赖、输出位置。
- 论文中的 FSF-guided slicing：`ForwardSlice(input) ∩ BackwardSlice(output)`、依赖闭包、`T` 下不可达分支证明与剪枝、Java 源码重建。
- 对每个切片调用 `javac`，把“形式上的切片”升级为经过编译验证的可执行切片。
- TBFV 迭代：Z3 生成满足 `T ∧ ¬C₁ ∧ ... ∧ ¬Cₖ` 的测试，具体/符号同步执行，记录路径条件 `Cᵢ` 和输出状态表示 `y=fᵢ(x)`。
- Soundness 判定：`T ∧ Cᵢ ⇒ D(fᵢ(x)/y)`。
- Completeness 判定：`∃x(T ∧ D) ⇒ ∨ᵢ∃x(T ∧ Cᵢ ∧ y=fᵢ(x))`。
- `sound / locally_sound / unsound`、`complete / locally_complete / incomplete / inconclusive` 分级，不把路径/循环截断伪装成全局证明。
- 原程序与切片使用相同参数重复验证，报告判断保持情况。
- LOC、可执行语句数、圈复杂度、路径数、路径条件、测试数据、反例和耗时的 JSON + HTML 报告。
- 可选 OpenAI-compatible LLM FSF 草拟；必须显式传入 `--allow-llm`，密钥只从环境变量读取。
- 随包数据集检查命令；当前提供的数据集中 301 个 Java 文件有 300 个可以被解析，唯一失败文件本身缺少类结束大括号，`javac` 同样拒绝该文件。

## 环境

- Python 3.10+
- Java/JDK 17+（只在切片编译验证时需要）
- macOS、Linux 或 Windows

核心依赖固定在 `requirements.txt`：`javalang`、`PyYAML`、`z3-solver`。

## 安装

macOS / Linux：

```bash
./install.sh
.venv/bin/fsf-tbfv doctor
```

Windows PowerShell：

```powershell
./install.ps1
.venv/Scripts/fsf-tbfv.exe doctor
```

也可以手动安装：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

## 立即运行

完整切片 + TBFV + 原程序对照 + 报告：

```bash
.venv/bin/fsf-tbfv analyze \
  --java examples/UserInputProgram.java \
  --fsf examples/cube_sum.fsf.yaml \
  --output demo-output
```

结果包括：

```text
demo-output/
├── report.json
├── report.html
└── slices/
    ├── T_nonpositive/UserInputProgram.java
    └── T_positive/UserInputProgram.java
```

论文中的 calculator 场景也已经准备好：

```bash
.venv/bin/fsf-tbfv analyze \
  --java examples/Calculator.java \
  --fsf examples/calculator.fsf.yaml \
  --output calculator-output
```

## 命令

```text
doctor          检查 Python、Z3、javalang、javac
init-fsf        从 Java 方法生成可编辑的 FSF YAML 骨架
validate-fsf    检查 FSF 语法、变量、互斥性和输入域覆盖
slice           只执行 FSF-guided slicing，并编译切片
verify          只对给定程序执行 TBFV
analyze         完整流水线：校验、切片、编译、TBFV、原/切片对照、报告
dataset-check   扫描一个 Java 数据集，列出可解析项和失败原因
suggest-fsf     可选 LLM 草拟 FSF；形式化校验仍由本地工具完成
```

为任意 Java 文件建立 FSF：

```bash
.venv/bin/fsf-tbfv init-fsf \
  --java datasets/PCaE-Dataset/Branched3/FizzBuzz_Original.java \
  --method fizzBuzz \
  --output fizzbuzz.fsf.yaml
```

数据集审计：

```bash
.venv/bin/fsf-tbfv dataset-check \
  --java-dir datasets/PCaE-Dataset \
  --output dataset-check.json
```

## FSF 文件

```yaml
method: calculate
inputs:
  num1: {type: int, min: -20, max: 20}
  num2: {type: int, min: -20, max: 20}
  operator: {type: char, min: 37, max: 47}
outputs:
  return_value: {type: int, source: return}
scenarios:
  - id: T_div
    T: "operator == '/' && num2 != 0"
    D: "return_value == num1 / num2"
analysis:
  max_paths: 128
  max_loop_iterations: 128
  solver_timeout_ms: 10000
  compare_original: true
  compile_slices: true
```

表达式使用 Java 风格：`&&`、`||`、`!`、比较、`+ - * / %`、位运算、三目表达式和 `Math.abs/min/max`。`int` 与 `long` 使用 Java 有符号位向量语义，包括溢出和负数余数。`float/double` 在验证层使用精确实数近似；因此依赖 IEEE-754 NaN、Infinity、舍入误差的结论应视为模型近似。

输入 `min/max` 定义本次 TBFV 的分析域。论文中的测试阶段同样需要可终止的测试条件，例如把 `x>0` 收窄为 `0<x<=500`。若未填写，工具默认对数值输入采用 `[-100,100]`。输出 `min/max` 不是 soundness 所必需，但在带溢出的 completeness 公式中可以明确待分析的输出域。

## 判断含义

- `sound`：所有 `T` 输入均被完整路径覆盖，每条路径都满足 `D`。
- `locally_sound`：所有已探索路径满足 `D`，但路径条件尚未覆盖全部 `T`。
- `unsound`：存在由 Z3 给出的输入反例，使程序输出违反 `D`，或执行触发未由场景允许的异常。
- `complete`：`D` 允许的每个输出都能由某个已探索的 `T` 输入产生。
- `incomplete`：路径已经覆盖全部 `T`，但存在 `D` 允许而程序不可达的输出反例。
- `locally_complete`：在已探索区域内发现未覆盖输出，但由于 `T` 尚未完整覆盖，不能作全局 incomplete 判断。
- `inconclusive`：遇到超时或当前标量 Java 模型不支持的语法/调用。

## 有界性与可信边界

TBFV 的优势是不用人工提供循环不变式；代价是它依赖测试诱导路径。工具严格遵守论文的“全路径覆盖后才给全局判断”原则：

- 达到 `max_paths` 或 `max_loop_iterations` 时，报告会标记 partial/local 或 inconclusive。
- Z3 `unknown` 不会被当作 `unsat`。
- 每个切片会被 `javac` 编译；编译失败保留完整错误信息。
- 原程序和切片默认在相同 FSF、输入域、路径上限和 solver 配置下分别验证。

当前执行器面向论文和 PCaE 数据集中的标量 Java 子集，支持顺序、分支、`switch`、`while`、`do-while`、普通 `for`、`break/continue/return/throw`、整数/实数/布尔/字符以及常见 `Math` 函数。数组、集合、对象图、递归、跨方法符号执行、字符串语义和复杂库调用会明确返回 `inconclusive`；切片器仍会进行保守依赖分析。论文自身也把复杂数据结构、方法调用和丰富 Java 特性列为当前方法的扩展方向。

## 可选 LLM

```bash
export FSF_LLM_API_KEY='...'
.venv/bin/fsf-tbfv suggest-fsf \
  --java MyProgram.java \
  --method targetMethod \
  --model your-model \
  --base-url https://api.example.com/v1 \
  --output MyProgram.fsf.yaml \
  --allow-llm
```

生成后必须运行 `validate-fsf` 或 `analyze`。LLM 输出不是证明；Z3 与路径验证结果才是工具的判定依据。

## 测试

```bash
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest
```

更详细的论文到实现映射见 `docs/ALGORITHM.md`，FSF 字段说明见 `docs/FSF_FORMAT.md`，材料审计与复现边界见 `docs/REPRODUCTION_NOTES.md`。

