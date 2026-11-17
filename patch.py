import os, glob, sys

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
print("GreenApi patched")

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
            print("IntegrityVerifier patched", p)

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
            print("x22.a patched", p)

print("All patches done")
