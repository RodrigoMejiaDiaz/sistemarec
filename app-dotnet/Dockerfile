# Dockerfile-dotnet
FROM --platform=${BUILDPLATFORM} mcr.microsoft.com/dotnet/sdk:7.0 as build
ARG TARGETPLATFORM
ARG TARGETARCH
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

ENV REDIS_URL="localhost:6379"

WORKDIR /source
COPY *.csproj .
RUN dotnet restore -a $TARGETARCH

COPY Program.cs .
RUN dotnet publish -c release -o /app -a $TARGETARCH --self-contained false --no-restore

FROM mcr.microsoft.com/dotnet/runtime:7.0
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "Worker.dll"]
