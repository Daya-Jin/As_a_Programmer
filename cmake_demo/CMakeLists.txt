cmake_minimum_required(VERSION 3.19)    # cmake最低版本要求
project(cpp_proj)    # 项目名

set(CMAKE_CXX_STANDARD 17)    # c++标准

include_directories(include)   # include头文件目录
link_directories(lib)    # 链接库目录

add_executable(cpp_proj main.cpp)    # 所有可执行文件

target_link_libraries(cpp_proj test)    # 必须在add_executable之后
