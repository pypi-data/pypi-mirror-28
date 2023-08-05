import sys
import traceback
from .cli import parser
from .jupiter.jupiter import Jupiter
from .jupiter.jupiter import test


def main(argv=sys.argv):

    if len(argv) < 2:
        parser.parse_args(["-h"])
        sys.exit(0)

    # 自動でコマンドライン引数を読み取る 引数必要なし
    args = parser.parse_args()

    try:
        # exit_code = program(args)
        exit_code = test()
        sys.exit(exit_code)

    except Exception as e:
        error_type = type(e).__name__
        stack_trace = traceback.format_exc()

        if args.stacktrace:
            print("{:=^30}".format(" STACK TRACE "))
            print(stack_trace.strip())

        else:
            sys.stderr.write(
                "{0}: {1}\n".format(e_type, e.message))
            sys.exit(1)

# def get_agents_list():
#     agents = os.listdir('agents/')
#     print(agents)
#
# if __name__ == '__main__':
#     start = time.time()
#     simu = Jupiter(TypeOfNegotiation.Turn, 100, 'domain/Terra/NewDomain.xml',
#         'domain/Terra/NewDomain_util1.xml', 'domain/Terra/NewDomain_util2.xml', 'domain/Terra/NewDomain_util3.xml')
#
#
#     simu.set_improvement_agent()
#     simu.set_java_agent(25535)
#     simu.set_java_agent(25536)
#     for i in range(0, 1000):
#         simu.do_negotiation(is_printing=False, print_times=100)
#     simu.save_history_as_json()
