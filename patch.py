import os, glob, sys, re

# ========== 1. Crack key + integrity ==========
path = "green/smali_classes2/com/xyz/app/GreenApi.smali"
if not os.path.exists(path):
    path = "green/smali/com/xyz/app/GreenApi.smali"
if not os.path.exists(path):
    print("GreenApi.smali not found")
    sys.exit(1)

with open(path) as f:
    c = f.read()

start = c.find(".method public static validate(Ljava/lang/String;Z)Lcom/xyz/app/GreenApi$Result;")
if start == -1:
    print("validate method not found")
    sys.exit(1)

nextm = c.find("\n.method ", start + 10)
if nextm == -1:
    nextm = len(c)
end = c.rfind(".end method", start, nextm)

new = """.method public static validate(Ljava/lang/String;Z)Lcom/xyz/app/GreenApi$Result;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    new-instance v0, Lcom/xyz/app/GreenApi$Result;
    invoke-direct {v0}, Lcom/xyz/app/GreenApi$Result;-><init>()V
    const-wide/16 v1, 0x0
    iput-wide v1, v0, Lcom/xyz/app/GreenApi$Result;->expires:J
    const/4 v1, 0x0
    iput-boolean v1, v0, Lcom/xyz/app/GreenApi$Result;->force:Z
    const-string v1, ""
    iput-object v1, v0, Lcom/xyz/app/GreenApi$Result;->link:Ljava/lang/String;
    return-object v0
.end method
"""

c = c[:start] + new + c[end + len(".end method"):]

for sig, body in [
(".method public static consume(Lcom/xyz/app/GreenApi$Result;)V",
""".method public static consume(Lcom/xyz/app/GreenApi$Result;)V
    .registers 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation
    return-void
.end method
"""),
(".method public static log(Landroid/content/Context;Ljava/lang/String;)V",
""".method public static log(Landroid/content/Context;Ljava/lang/String;)V
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation
    return-void
.end method
""")
]:
    s = c.find(sig)
    if s != -1:
        nm = c.find("\n.method ", s + 10)
        if nm == -1:
            nm = len(c)
        e = c.rfind(".end method", s, nm)
        c = c[:s] + body + c[e + len(".end method"):]

with open(path, "w") as f:
    f.write(c)
print("[OK] GreenApi patched")

for pattern in ["green/smali/**/IntegrityVerifier.smali", "green/smali_classes*/**/IntegrityVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f:
            c = f.read()
        start = c.find(".method static verify(Ljava/io/File;[[BLjava/lang/String;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1:
                nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method static verify(Ljava/io/File;[[BLjava/lang/String;)Z
    .registers 3
    const/4 v0, 0x1
    return v0
.end method
"""
            c = c[:start] + new + c[end + len(".end method"):]
            with open(p, "w") as f:
                f.write(c)
            print("[OK] IntegrityVerifier", p)

for pattern in ["green/smali/**/x22/a.smali", "green/smali_classes*/**/x22/a.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f:
            c = f.read()
        start = c.find(".method public static a(Landroid/content/Context;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1:
                nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method public static a(Landroid/content/Context;)Z
    .registers 1
    const/4 v0, 0x1
    return v0
.end method
"""
            c = c[:start] + new + c[end + len(".end method"):]
            with open(p, "w") as f:
                f.write(c)
            print("[OK] x22.a", p)

print("[OK] Crack done")

# ========== 2. FULL Vietnamese - ONLY inside const-string ==========
# Only replace inside quoted strings of const-string lines to avoid breaking types/methods

replacements = [
    # LOGIN
    ("CENTRAL DE ACESSO / V12", "TRUNG TÂM TRUY CẬP / V12"),
    ("AUTENTICAR LICENCA", "XÁC THỰC KEY"),
    ("AUTENTICAR LICENÇA", "XÁC THỰC KEY"),
    ("Conecte sua key ao painel GREEN.", "Nhập key để kích hoạt GREEN."),
    ("VALIDAR ACESSO", "XÁC NHẬN"),
    ("OBTER KEY", "LẤY KEY"),
    ("GREEN MODZ  •  ACESSO POR KEY", "GREEN MODZ  •  MỞ BẰNG KEY"),
    ("Digite a key.", "Hãy nhập key."),
    ("Consultando sua key…", "Đang kiểm tra key…"),
    ("Consultando sua key...", "Đang kiểm tra key..."),
    ("VERIFICANDO…", "ĐANG KIỂM TRA…"),
    ("VERIFICANDO...", "ĐANG KIỂM TRA..."),
    ("Não foi possível validar. Confira sua conexão e tente novamente.", "Không thể xác thực. Kiểm tra mạng rồi thử lại."),
    ("Não foi possível abrir a tela principal.", "Không thể mở màn hình chính."),
    ("Não foi possível abrir o link. Verifique seu navegador.", "Không thể mở link. Kiểm tra trình duyệt."),
    ("Atualização disponível", "Có bản cập nhật"),
    ("Atualize o GREEN V12 para continuar.", "Cập nhật GREEN V12 để tiếp tục."),
    ("Atualizar", "Cập nhật"),
    ("Sair", "Thoát"),

    # SESSION
    ("Key ativa • Sem validade", "Key đang hoạt động • Không hết hạn"),
    ("Key ativa", "Key đang hoạt động"),
    ("Sem validade", "Không hết hạn"),
    ("Validade  ", "Hạn dùng  "),
    ("Validade", "Hạn dùng"),
    (" • Sem conexão", " • Mất mạng"),
    ("Sem conexão", "Mất mạng"),
    ("Key expirada", "Key đã hết hạn"),
    ("Atualize o aplicativo para continuar", "Cập nhật ứng dụng để tiếp tục"),

    # MAIN UI
    ("Instalar", "Cài đặt"),
    ("INSTALAR", "CÀI ĐẶT"),
    ("Launch", "Mở game"),
    ("LAUNCH", "MỞ GAME"),
    ("Iniciar", "Khởi động"),
    ("INICIAR", "KHỞI ĐỘNG"),
    ("Status", "Trạng thái"),
    ("STATUS", "TRẠNG THÁI"),
    ("Pronto", "Sẵn sàng"),
    ("PRONTO", "SẴN SÀNG"),
    ("Aguardando", "Đang chờ"),
    ("AGUARDANDO", "ĐANG CHỜ"),
    ("Conectado", "Đã kết nối"),
    ("CONECTADO", "ĐÃ KẾT NỐI"),
    ("Desconectado", "Mất kết nối"),
    ("DESCONECTADO", "MẤT KẾT NỐI"),
    ("Erro", "Lỗi"),
    ("ERRO", "LỖI"),
    ("Sucesso", "Thành công"),
    ("SUCESSO", "THÀNH CÔNG"),
    ("Carregando", "Đang tải"),
    ("CARREGANDO", "ĐANG TẢI"),
    ("Processando", "Đang xử lý"),
    ("PROCESSANDO", "ĐANG XỬ LÝ"),
    ("Concluído", "Hoàn thành"),
    ("CONCLUÍDO", "HOÀN THÀNH"),
    ("Falhou", "Thất bại"),
    ("FALHOU", "THẤT BẠI"),
    ("Tentar novamente", "Thử lại"),
    ("TENTE NOVAMENTE", "THỬ LẠI"),
    ("Cancelar", "Hủy"),
    ("CANCELAR", "HỦY"),
    ("Confirmar", "Xác nhận"),
    ("CONFIRMAR", "XÁC NHẬN"),
    ("Fechar", "Đóng"),
    ("FECHAR", "ĐÓNG"),

    # ADB / PAIR
    ("Pareamento", "Ghép nối"),
    ("PAREAMENTO", "GHÉP NỐI"),
    ("Parear", "Ghép nối"),
    ("Depuração sem fio", "Gỡ lỗi không dây"),
    ("Código de pareamento", "Mã ghép nối"),

    # MODULE
    ("Módulo", "Module"),
    ("MÓDULO", "MODULE"),
    ("Instalando módulo", "Đang cài module"),
    ("Módulo instalado", "Module đã cài"),
    ("Falha na instalação", "Cài đặt thất bại"),
    ("Arquivo não encontrado", "Không tìm thấy file"),
    ("Permissão negada", "Bị từ chối quyền"),
    ("Permissão", "Quyền"),
    ("PERMISSÃO", "QUYỀN"),

    # MENU
    ("Configurações", "Cài đặt"),
    ("CONFIGURAÇÕES", "CÀI ĐẶT"),
    ("Opções", "Tùy chọn"),
    ("OPÇÕES", "TÙY CHỌN"),
    ("Ativar", "Bật"),
    ("ATIVAR", "BẬT"),
    ("Desativar", "Tắt"),
    ("DESATIVAR", "TẮT"),
    ("Ligado", "Bật"),
    ("Desligado", "Tắt"),

    # ERRORS
    ("Limite de usos atingido", "Đã hết lượt sử dụng"),
    ("Aplicativo indisponível no painel", "Ứng dụng không khả dụng"),
    ("GREEN V12 não encontrado no painel", "Không tìm thấy GREEN V12"),
    ("Identificador de key inválido", "Key không hợp lệ"),
    ("Key inválida", "Key không hợp lệ"),
    ("Key invalida", "Key không hợp lệ"),
    ("Conexão perdida", "Mất kết nối"),
    ("Tempo esgotado", "Hết thời gian"),
    ("Falha na conexão", "Kết nối thất bại"),
    ("Sem internet", "Không có mạng"),
    ("Verifique sua conexão", "Kiểm tra kết nối mạng"),
    ("Tente novamente mais tarde", "Thử lại sau"),
    ("Algo deu errado", "Đã xảy ra lỗi"),
    ("Operação cancelada", "Đã hủy thao tác"),
    ("Aguarde", "Vui lòng đợi"),
    ("AGUARDE", "VUI LÒNG ĐỢI"),

    # COMMON
    ("Acesso", "Truy cập"),
    ("ACESSO", "TRUY CẬP"),
    ("Licença", "Key"),
    ("LICENÇA", "KEY"),
    ("Licenca", "Key"),
    ("LICENCA", "KEY"),
    ("Painel", "Bảng điều khiển"),
    ("PAINEL", "BẢNG ĐIỀU KHIỂN"),
    ("Versão", "Phiên bản"),
    ("VERSÃO", "PHIÊN BẢN"),
    ("Versao", "Phiên bản"),
    ("Sobre", "Giới thiệu"),
    ("SOBRE", "GIỚI THIỆU"),
    ("Ajuda", "Trợ giúp"),
    ("AJUDA", "TRỢ GIÚP"),
    ("Suporte", "Hỗ trợ"),
    ("SUPORTE", "HỖ TRỢ"),
    ("Canal", "Kênh"),
    ("CANAL", "KÊNH"),
    ("Grupo", "Nhóm"),
    ("GRUPO", "NHÓM"),
    ("Baixar", "Tải xuống"),
    ("BAIXAR", "TẢI XUỐNG"),
    ("Atualizado", "Đã cập nhật"),
    ("ATUALIZADO", "ĐÃ CẬP NHẬT"),
    ("Novo", "Mới"),
    ("NOVO", "MỚI"),
    ("Estável", "Ổn định"),
    ("ESTÁVEL", "ỔN ĐỊNH"),
]

def translate_const_strings(content, pairs):
    """Only replace text inside const-string \"...\"  lines"""
    def replacer(match):
        full = match.group(0)
        # extract the string part
        q1 = full.find('"')
        q2 = full.rfind('"')
        if q1 == -1 or q2 <= q1:
            return full
        prefix = full[:q1+1]
        s = full[q1+1:q2]
        suffix = full[q2:]
        for old, new in pairs:
            if old in s:
                s = s.replace(old, new)
        return prefix + s + suffix

    # match const-string lines (with optional register)
    pattern = re.compile(r'const-string(?:/jumbo)?\s+v\d+,\s*".*?"', re.DOTALL)
    return pattern.sub(replacer, content)

count = 0
for root, dirs, files in os.walk("green"):
    for name in files:
        if not name.endswith(".smali") and not name.endswith(".xml"):
            continue
        full = os.path.join(root, name)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            original = content

            if name.endswith(".smali"):
                content = translate_const_strings(content, replacements)
            else:
                # xml: safe full replace
                for old, new in replacements:
                    content = content.replace(old, new)

            if content != original:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
        except Exception:
            pass

print(f"[OK] Full Vietnamese translation done ({count} files changed)")
print("[OK] All patches finished")
