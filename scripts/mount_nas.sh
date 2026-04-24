#!/bin/bash
#===============================================================================
# NAS 挂载配置脚本
# 在 Linux 虚拟机上运行，用于配置 NAS 存储挂载
#
# 用法:
#   ./mount_nas.sh                    - 交互式配置（推荐首次使用）
#   ./mount_nas.sh --nfs IP:/path     - 快速挂载 NFS
#   ./mount_nas.sh --smb IP/share     - 快速挂载 SMB
#   ./mount_nas.sh --unmount          - 卸载所有 NAS 挂载
#   ./mount_nas.sh --check            - 检查挂载状态
#===============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认挂载点
RAW_MOUNT_POINT="/mnt/nas/raw"
CLEANED_MOUNT_POINT="/mnt/nas/cleaned"

#===============================================================================
# 检查依赖
#===============================================================================

check_dependencies() {
    echo -e "${BLUE}检查依赖...${NC}"

    if [ "$(id -u)" -ne 0 ]; then
        echo -e "${RED}错误: 请使用 sudo 运行此脚本${NC}"
        exit 1
    fi

    local missing=""

    # 检查 NFS 工具
    if ! command -v mount.nfs &> /dev/null; then
        missing="$missing nfs-common"
    fi

    # 检查 SMB 工具
    if ! command -v mount.cifs &> /dev/null; then
        missing="$missing cifs-utils"
    fi

    if [ -n "$missing" ]; then
        echo -e "${YELLOW}缺少依赖，正在安装...${NC}"
        apt update
        apt install -y $missing
    fi

    echo -e "${GREEN}依赖检查完成${NC}"
}

#===============================================================================
# 创建挂载点
#===============================================================================

create_mount_points() {
    echo -e "${BLUE}创建挂载点...${NC}"

    mkdir -p "$RAW_MOUNT_POINT"
    mkdir -p "$CLEANED_MOUNT_POINT"
    mkdir -p "$CLEANED_MOUNT_POINT/logs"

    echo -e "${GREEN}挂载点创建完成${NC}"
}

#===============================================================================
# 挂载 NFS
#===============================================================================

mount_nfs() {
    local nas_ip=$1
    local raw_path=$2
    local cleaned_path=$3

    echo -e "${BLUE}挂载 NFS 存储...${NC}"
    echo "  NAS IP: $nas_ip"
    echo "  原始数据路径: $raw_path"
    echo "  清洗后路径: $cleaned_path"

    # 挂载原始数据
    echo -e "${YELLOW}挂载原始数据目录...${NC}"
    if mountpoint -q "$RAW_MOUNT_POINT"; then
        echo -e "${GREEN}原始数据目录已挂载，跳过${NC}"
    else
        mount -t nfs "${nas_ip}:${raw_path}" "$RAW_MOUNT_POINT" -o rw,hard,intr,timeo=600,retrans=2
        echo -e "${GREEN}原始数据目录挂载成功${NC}"
    fi

    # 挂载清洗后目录
    echo -e "${YELLOW}挂载清洗后目录...${NC}"
    if mountpoint -q "$CLEANED_MOUNT_POINT"; then
        echo -e "${GREEN}清洗后目录已挂载，跳过${NC}"
    else
        mount -t nfs "${nas_ip}:${cleaned_path}" "$CLEANED_MOUNT_POINT" -o rw,hard,intr,timeo=600,retrans=2
        echo -e "${GREEN}清洗后目录挂载成功${NC}"
    fi

    # 添加到 fstab
    echo -e "${YELLOW}配置开机自动挂载...${NC}"
    add_to_fstab_nfs "$nas_ip" "$raw_path" "$cleaned_path"

    echo -e "${GREEN}NFS 挂载完成！${NC}"
}

#===============================================================================
# 挂载 SMB/CIFS
#===============================================================================

mount_smb() {
    local nas_ip=$1
    local raw_share=$2
    local cleaned_share=$3
    local username=$4
    local password=$5

    echo -e "${BLUE}挂载 SMB/CIFS 存储...${NC}"
    echo "  NAS IP: $nas_ip"
    echo "  原始数据共享: $raw_share"
    echo "  清洗后共享: $cleaned_share"

    # 创建凭据文件
    local cred_file="/root/.nas_credentials"
    echo "username=$username" > "$cred_file"
    echo "password=$password" >> "$cred_file"
    chmod 600 "$cred_file"

    # 挂载原始数据
    echo -e "${YELLOW}挂载原始数据目录...${NC}"
    if mountpoint -q "$RAW_MOUNT_POINT"; then
        echo -e "${GREEN}原始数据目录已挂载，跳过${NC}"
    else
        mount -t cifs "//${nas_ip}/${raw_share}" "$RAW_MOUNT_POINT" \
            -o credentials="$cred_file",iocharset=utf8,uid=1000,gid=1000
        echo -e "${GREEN}原始数据目录挂载成功${NC}"
    fi

    # 挂载清洗后目录
    echo -e "${YELLOW}挂载清洗后目录...${NC}"
    if mountpoint -q "$CLEANED_MOUNT_POINT"; then
        echo -e "${GREEN}清洗后目录已挂载，跳过${NC}"
    else
        mount -t cifs "//${nas_ip}/${cleaned_share}" "$CLEANED_MOUNT_POINT" \
            -o credentials="$cred_file",iocharset=utf8,uid=1000,gid=1000
        echo -e "${GREEN}清洗后目录挂载成功${NC}"
    fi

    # 添加到 fstab
    echo -e "${YELLOW}配置开机自动挂载...${NC}"
    add_to_fstab_smb "$nas_ip" "$raw_share" "$cleaned_share"

    echo -e "${GREEN}SMB 挂载完成！${NC}"
}

#===============================================================================
# 添加到 fstab (NFS)
#===============================================================================

add_to_fstab_nfs() {
    local nas_ip=$1
    local raw_path=$2
    local cleaned_path=$3

    # 备份 fstab
    cp /etc/fstab /etc/fstab.bak

    # 添加 NFS 挂载项
    if ! grep -q "${nas_ip}:${raw_path}" /etc/fstab; then
        echo "${nas_ip}:${raw_path} ${RAW_MOUNT_POINT} nfs rw,hard,intr,timeo=600,retrans=2,_netdev 0 0" >> /etc/fstab
    fi

    if ! grep -q "${nas_ip}:${cleaned_path}" /etc/fstab; then
        echo "${nas_ip}:${cleaned_path} ${CLEANED_MOUNT_POINT} nfs rw,hard,intr,timeo=600,retrans=2,_netdev 0 0" >> /etc/fstab
    fi

    echo -e "${GREEN}fstab 配置已更新${NC}"
}

#===============================================================================
# 添加到 fstab (SMB)
#===============================================================================

add_to_fstab_smb() {
    local nas_ip=$1
    local raw_share=$2
    local cleaned_share=$3
    local cred_file="/root/.nas_credentials"

    # 备份 fstab
    cp /etc/fstab /etc/fstab.bak

    # 添加 SMB 挂载项
    if ! grep -q "//${nas_ip}/${raw_share}" /etc/fstab; then
        echo "//${nas_ip}/${raw_share} ${RAW_MOUNT_POINT} cifs credentials=${cred_file},iocharset=utf8,uid=1000,gid=1000,_netdev 0 0" >> /etc/fstab
    fi

    if ! grep -q "//${nas_ip}/${cleaned_share}" /etc/fstab; then
        echo "//${nas_ip}/${cleaned_share} ${CLEANED_MOUNT_POINT} cifs credentials=${cred_file},iocharset=utf8,uid=1000,gid=1000,_netdev 0 0" >> /etc/fstab
    fi

    echo -e "${GREEN}fstab 配置已更新${NC}"
}

#===============================================================================
# 卸载 NAS
#===============================================================================

unmount_nas() {
    echo -e "${YELLOW}卸载 NAS 挂载...${NC}"

    if mountpoint -q "$RAW_MOUNT_POINT"; then
        umount "$RAW_MOUNT_POINT"
        echo -e "${GREEN}已卸载: $RAW_MOUNT_POINT${NC}"
    fi

    if mountpoint -q "$CLEANED_MOUNT_POINT"; then
        umount "$CLEANED_MOUNT_POINT"
        echo -e "${GREEN}已卸载: $CLEANED_MOUNT_POINT${NC}"
    fi

    # 询问是否删除 fstab 条目
    read -p "是否从 fstab 中删除 NAS 挂载项? (y/n): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        # 保留备份，删除相关行
        grep -v "/mnt/nas/raw\|/mnt/nas/cleaned" /etc/fstab > /etc/fstab.tmp
        mv /etc/fstab.tmp /etc/fstab
        echo -e "${GREEN}fstab 条目已删除${NC}"
    fi

    echo -e "${GREEN}卸载完成${NC}"
}

#===============================================================================
# 检查挂载状态
#===============================================================================

check_mount() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  NAS 挂载状态${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    echo -e "${BLUE}挂载点:${NC}"
    echo "  $RAW_MOUNT_POINT:"
    if mountpoint -q "$RAW_MOUNT_POINT"; then
        echo -e "    ${GREEN}已挂载${NC}"
        df -h "$RAW_MOUNT_POINT" | tail -1 | awk '{printf "    使用: %s / %s (%s)\n", $3, $2, $5}'
    else
        echo -e "    ${RED}未挂载${NC}"
    fi

    echo ""
    echo "  $CLEANED_MOUNT_POINT:"
    if mountpoint -q "$CLEANED_MOUNT_POINT"; then
        echo -e "    ${GREEN}已挂载${NC}"
        df -h "$CLEANED_MOUNT_POINT" | tail -1 | awk '{printf "    使用: %s / %s (%s)\n", $3, $2, $5}'
    else
        echo -e "    ${RED}未挂载${NC}"
    fi

    echo ""

    # 显示 NFS/SMB 连接
    echo -e "${BLUE}当前挂载的 NAS 设备:${NC}"
    mount | grep -E "nfs|cifs|/mnt/nas" || echo "  无"
}

#===============================================================================
# 交互式配置
#===============================================================================

interactive_setup() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  NAS 挂载配置向导${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    # 选择挂载类型
    echo "请选择 NAS 挂载类型:"
    echo "  1) NFS（推荐，用于 Linux 服务器）"
    echo "  2) SMB/CIFS（用于 Windows NAS 或混合环境）"
    echo "  3) 直接映射（如果 NAS 已挂载在其他位置）"
    read -p "请选择 [1/2/3]: " mount_type

    case $mount_type in
        1)
            read -p "NAS IP 地址: " nas_ip
            read -p "NAS 上原始数据路径 (如 /nas/raw): " raw_path
            read -p "NAS 上清洗后数据路径 (如 /nas/cleaned): " cleaned_path
            mount_nfs "$nas_ip" "$raw_path" "$cleaned_path"
            ;;
        2)
            read -p "NAS IP 地址: " nas_ip
            read -p "NAS 上原始数据共享名 (如 nas_raw): " raw_share
            read -p "NAS 上清洗后数据共享名 (如 nas_cleaned): " cleaned_share
            read -p "NAS 用户名: " nas_user
            read -s -p "NAS 密码: " nas_pass
            echo ""
            mount_smb "$nas_ip" "$raw_share" "$cleaned_share" "$nas_user" "$nas_pass"
            ;;
        3)
            echo -e "${YELLOW}直接映射模式${NC}"
            read -p "现有挂载点路径: " existing_mount
            read -p "映射为原始数据目录 ($RAW_MOUNT_POINT)? (y/n): " confirm
            if [ "$confirm" = "y" ]; then
                ln -sf "$existing_mount" "$RAW_MOUNT_POINT"
            fi
            read -p "清洗后目录现有路径: " existing_cleaned
            ln -sf "$existing_cleaned" "$CLEANED_MOUNT_POINT"
            echo -e "${GREEN}映射完成${NC}"
            ;;
        *)
            echo -e "${RED}无效选择${NC}"
            exit 1
            ;;
    esac
}

#===============================================================================
# 主入口
#===============================================================================

show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --nfs IP:/raw_path:/cleaned_path    快速 NFS 挂载"
    echo "  --smb IP:share:share:user:pass     快速 SMB 挂载"
    echo "  --unmount                           卸载所有 NAS 挂载"
    echo "  --check                             检查挂载状态"
    echo "  --help, -h                          显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 --nfs 192.168.1.10:/nas/raw:/nas/cleaned"
    echo "  $0 --smb 192.168.1.10:nas_raw:nas_cleaned:admin:password"
    echo "  $0 --check"
}

case ${1:-""} in
    --nfs)
        IFS=':' read -r nas_ip raw_path cleaned_path <<< "$2"
        check_dependencies
        create_mount_points
        mount_nfs "$nas_ip" "$raw_path" "$cleaned_path"
        ;;
    --smb)
        IFS=':' read -r nas_ip raw_share cleaned_share username password <<< "$2"
        check_dependencies
        create_mount_points
        mount_smb "$nas_ip" "$raw_share" "$cleaned_share" "$username" "$password"
        ;;
    --unmount)
        unmount_nas
        ;;
    --check)
        check_mount
        ;;
    --help|-h)
        show_help
        ;;
    "")
        check_dependencies
        create_mount_points
        interactive_setup
        ;;
    *)
        echo -e "${RED}未知参数: $1${NC}"
        show_help
        exit 1
        ;;
esac
