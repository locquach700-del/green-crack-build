import os, re

# ========== 2. FULL Vietnamese - ONLY inside const-string ==========
# Only replace inside quoted strings of const-string lines to avoid breaking types/methods

replacements = [
    ("LA conexão ADB foi desconectada. Ative a depuração sem fio e reconecte o ADB.", "Kết nối ADB đã bị ngắt. Bật gỡ lỗi không dây rồi kết nối lại ADB."),
    ("QA pasta do jogo está inacessível. Autorize o acesso nas configurações ou use ADB.", "Thư mục trò chơi không thể truy cập. Cấp quyền trong cài đặt hoặc dùng ADB."),
    ("A resposta do ADB é muito longa..", "Phản hồi ADB quá dài."),
    ("!A resposta do ADB é muito longa..", "Phản hồi ADB quá dài."),
    ("ADB CONECTADO. PROXY ATIVO pronto para abrir..", "ADB ĐÃ KẾT NỐI. PROXY ĐANG BẬT, SẴN SÀNG MỞ.."),
    ("ADB CONECTADO. Toque em INJETAR PROXY.", "ADB ĐÃ KẾT NỐI. Chạm vào INJECT PROXY."),
    ("ADB conectado. Volte ao GREEN V12 e toque em PREPARAR ARQUIVOS.", "ADB đã kết nối. Quay lại GREEN V12 và chạm vào CHUẨN BỊ TỆP."),
    ("ADB desconectado. Reconecte o ADB..", "ADB đã ngắt kết nối. Kết nối lại ADB.."),
    ("ADB desconectado. Toque em ATIVAR ou reconecte..", "ADB đã ngắt kết nối. Chạm vào BẬT hoặc kết nối lại.."),
    ("ADB mengakhiri respons sebelum konfirmasi.", "ADB kết thúc phản hồi trước khi xác nhận."),
    ("Abra Depuração sem fio > Parear com código. Expanda a notificação GREEN V12 e toque em DIGITAR CÓDIGO, ou digite pelo aplicativo.", "Mở Gỡ lỗi không dây > Ghép nối bằng mã. Mở rộng thông báo GREEN V12 và chạm NHẬP MÃ, hoặc nhập trong ứng dụng."),
    ("Abra Parear com código no Android em tela dividida e digite os seis números:", "Mở Ghép nối bằng mã trên Android ở chế độ chia đôi màn hình rồi nhập sáu chữ số:"),
    ("AIM FOV SIZE harus 1–100.", "KÍCH THƯỚC FOV NGẮM phải từ 1–100."),
    ("AIM FOV SIZE 1 sampai 100 persen", "KÍCH THƯỚC FOV NGẮM từ 1 đến 100%"),
    ("Fechar e remover o flutuante", "Đóng và gỡ nút nổi"),
    ("Servidor indisponível (HTTP", "Máy chủ không khả dụng (HTTP"),
    ("Resposta muito grande", "Phản hồi quá lớn"),
    ("Minimizar menu", "Thu nhỏ menu"),
    ("Minimizar", "Thu nhỏ"),
    ("Menu flutuante ativo", "Menu nổi đang bật"),
    ("AIMBOT HEAD", "NHẮM ĐẦU"),
    ("AIMLOCK BODY", "KHÓA NGẮM THÂN"),
    ("AIM FOV SIZE", "KÍCH THƯỚC FOV NGẮM"),
    ("AIM FOV", "FOV NGẮM"),
    ("AJUSTES", "CÀI ĐẶT"),
    ("ADB CONECTADO", "ADB ĐÃ KẾT NỐI"),
    ("PAREAMENTO ADB", "GHÉP NỐI ADB"),
    ("PRONTAS PARA ATIVAR", "SẴN SÀNG KÍCH HOẠT"),
    ("DRAG HS", "KÉO TÂM HS"),
    ("DRAG", "KÉO TÂM"),
    ("Accept", "Chấp nhận"),
    ("accept", "Chấp nhận"),
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
        for old, new in sorted(pairs, key=lambda pair: len(pair[0]), reverse=True):
            if old in s:
                s = s.replace(old, new)
        return prefix + s + suffix

    # match const-string lines (with optional register)
    pattern = re.compile(r'const-string(?:/jumbo)?\s+v\d+,\s*".*?"', re.DOTALL)
    return pattern.sub(replacer, content)

count = 0
for root, dirs, files in os.walk("decoded"):
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
                for old, new in sorted(replacements, key=lambda pair: len(pair[0]), reverse=True):
                    content = content.replace(old, new)

            if content != original:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
        except Exception:
            pass

print(f"[OK] Vietnamese translation done ({count} files changed)")
print("[OK] All patches finished")
