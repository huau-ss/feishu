"""
个性化知识检索引擎
支持共享知识库 + 个人 Obsidian 知识库 + 知识图谱的融合检索
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from core.rag_engine import RAGResult
from core.embedding import get_embedding_model
from vectorstore.vector_store import get_vector_store
from database import get_db_session

logger = logging.getLogger(__name__)


@dataclass
class PersonalRAGConfig:
    """个人 RAG 配置"""
    use_shared_kb: bool = True
    use_personal_kb: bool = True
    use_knowledge_graph: bool = True
    use_memory: bool = True
    max_shared_chunks: int = 5
    max_personal_chunks: int = 3
    max_graph_entities: int = 5
    rerank: bool = True


class PersonalRAGEngine:
    """个性化 RAG 引擎"""

    def __init__(
        self,
        shared_collection: str = "knowledge_base",
        employee_id: str = None,
    ):
        self.employee_id = employee_id
        self.shared_collection = shared_collection
        self.embedding_model = get_embedding_model()
        self.vector_store = get_vector_store()

        self._config = PersonalRAGConfig()

    def set_config(self, config: PersonalRAGConfig):
        """设置配置"""
        self._config = config

    def query(
        self,
        question: str,
        session_id: str = None,
        tags: List[str] = None,
        top_k: int = 10,
    ) -> Dict[str, Any]:
        """
        融合检索：共享知识库 + 个人知识库 + 知识图谱 + 记忆
        """
        results = {
            "shared_chunks": [],
            "personal_chunks": [],
            "graph_entities": [],
            "memories": [],
            "final_context": "",
            "sources": [],
        }

        query_embedding = self.embedding_model.embed([question])[0]

        # 1. 检索共享知识库
        if self._config.use_shared_kb:
            shared_results = self._search_shared_kb(query_embedding, top_k)
            results["shared_chunks"] = shared_results
            logger.debug(f"Shared KB: found {len(shared_results)} chunks")

        # 2. 检索个人知识库 (Obsidian)
        if self._config.use_personal_kb and self.employee_id:
            personal_results = self._search_personal_kb(query_embedding, top_k)
            results["personal_chunks"] = personal_results
            logger.debug(f"Personal KB: found {len(personal_results)} chunks")

        # 3. 检索知识图谱
        if self._config.use_knowledge_graph and self.employee_id:
            graph_results = self._search_knowledge_graph(question)
            results["graph_entities"] = graph_results
            logger.debug(f"Knowledge Graph: found {len(graph_results)} entities")

        # 4. 检索个人记忆
        if self._config.use_memory and self.employee_id:
            memory_results = self._search_memory(question)
            results["memories"] = memory_results
            logger.debug(f"Personal Memory: found {len(memory_results)} items")

        # 5. 融合构建上下文
        results["final_context"] = self._build_context(results, question)
        results["sources"] = self._build_sources(results)

        return results

    def _search_shared_kb(
        self,
        query_embedding: List[float],
        top_k: int,
    ) -> List[Dict]:
        """搜索共享知识库"""
        try:
            results = self.vector_store.search(
                collection=self.shared_collection,
                query_vector=query_embedding,
                top_k=top_k,
            )
            return [
                {
                    "type": "shared_kb",
                    "content": r.get("payload", {}).get("content", ""),
                    "title": r.get("payload", {}).get("title", ""),
                    "score": r.get("score", 0),
                    "metadata": r.get("payload", {}),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Shared KB search failed: {e}")
            return []

    def _search_personal_kb(
        self,
        query_embedding: List[float],
        top_k: int,
    ) -> List[Dict]:
        """搜索个人知识库"""
        try:
            from core.personal_knowledge import PersonalNoteManager
            manager = PersonalNoteManager()

            notes = manager.get_notes_for_embedding(self.employee_id, limit=100)
            if not notes:
                return []

            note_embeddings = []
            note_ids = []
            for note in notes:
                if note.embedding_vector_id:
                    note_ids.append(note.id)
                    note_embeddings.append({
                        "id": note.id,
                        "content": note.content[:500],
                        "title": note.title,
                        "tags": note.tags or [],
                    })

            if not note_embeddings:
                return []

            personal_collection = f"personal_kb_{self.employee_id}"
            personal_results = self.vector_store.search(
                collection=personal_collection,
                query_vector=query_embedding,
                top_k=top_k,
            )

            return [
                {
                    "type": "personal_kb",
                    "content": r.get("payload", {}).get("content", ""),
                    "title": r.get("payload", {}).get("title", ""),
                    "score": r.get("score", 0),
                    "metadata": r.get("payload", {}),
                }
                for r in personal_results
            ]
        except Exception as e:
            logger.error(f"Personal KB search failed: {e}")
            return []

    def _search_knowledge_graph(self, question: str) -> List[Dict]:
        """搜索知识图谱"""
        try:
            from core.personal_knowledge import KnowledgeGraphManager
            manager = KnowledgeGraphManager(self.employee_id)

            keywords = self._extract_keywords(question)
            entities = []
            for keyword in keywords[:3]:
                related = manager.get_related_entities(
                    self.employee_id,
                    keyword,
                    depth=2,
                )
                entities.extend(related)

            seen = set()
            unique_entities = []
            for e in entities:
                if e["id"] not in seen:
                    seen.add(e["id"])
                    unique_entities.append(e)

            return unique_entities[: self._config.max_graph_entities]

        except Exception as e:
            logger.error(f"Knowledge graph search failed: {e}")
            return []

    def _search_memory(self, question: str) -> List[Dict]:
        """搜索个人记忆"""
        try:
            from core.personal_knowledge import PersonalMemoryManager
            manager = PersonalMemoryManager(self.employee_id)
            memories = manager.get_memories(min_confidence=0.5)

            relevant = []
            keywords = self._extract_keywords(question)
            for m in memories:
                if any(kw.lower() in m["content"].lower() for kw in keywords):
                    relevant.append(m)

            return relevant[:5]

        except Exception as e:
            logger.error(f"Memory search failed: {e}")
            return []

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        import re
        words = re.findall(r'[\w]{2,}', text.lower())
        stopwords = {
            "的", "了", "是", "在", "我", "有", "和", "就", "不", "人",
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
        }
        return [w for w in words if w not in stopwords and len(w) > 1]

    def _build_context(
        self,
        results: Dict[str, Any],
        question: str,
    ) -> str:
        """构建融合上下文"""
        context_parts = []

        if results["shared_chunks"]:
            context_parts.append("## 共享知识库")
            for i, chunk in enumerate(results["shared_chunks"][: self._config.max_shared_chunks], 1):
                content = chunk["content"]
                title = chunk.get("title", "未知文档")
                context_parts.append(f"\n[{i}] {title}:\n{content[:300]}...")

        if results["personal_chunks"]:
            context_parts.append("\n## 个人笔记 (Obsidian)")
            for i, chunk in enumerate(results["personal_chunks"][: self._config.max_personal_chunks], 1):
                content = chunk["content"]
                title = chunk.get("title", "未知笔记")
                context_parts.append(f"\n[{i}] {title}:\n{content[:300]}...")

        if results["graph_entities"]:
            context_parts.append("\n## 相关知识图谱")
            entity_names = [e["name"] for e in results["graph_entities"]]
            context_parts.append(f"相关概念: {', '.join(entity_names)}")

        if results["memories"]:
            context_parts.append("\n## 用户背景信息")
            for m in results["memories"]:
                context_parts.append(f"- {m['summary'] or m['content'][:100]}")

        return "\n".join(context_parts) if context_parts else ""

    def _build_sources(self, results: Dict[str, Any]) -> List[Dict]:
        """构建来源列表"""
        sources = []

        for chunk in results["shared_chunks"][:3]:
            sources.append({
                "type": chunk["type"],
                "title": chunk.get("title", "未知"),
                "content": chunk["content"][:100],
                "score": chunk.get("score", 0),
            })

        for chunk in results["personal_chunks"][:2]:
            sources.append({
                "type": chunk["type"],
                "title": chunk.get("title", "未知"),
                "content": chunk["content"][:100],
                "score": chunk.get("score", 0),
            })

        return sources

    def sync_personal_kb(self) -> Dict[str, Any]:
        """同步个人知识库"""
        try:
            from core.personal_knowledge import (
                ObsidianVaultManager,
                ObsidianSyncer,
                PersonalNoteManager,
            )

            if not self.employee_id:
                return {"status": "error", "message": "No employee_id"}

            vault_manager = ObsidianVaultManager()
            vaults = vault_manager.get_by_employee(self.employee_id)

            if not vaults:
                return {"status": "no_vaults"}

            total_synced = 0
            for vault in vaults:
                syncer = ObsidianSyncer(vault)
                result = syncer.sync()
                total_synced += result.get("notes_added", 0) + result.get("notes_updated", 0)
                vault_manager.update_last_sync(vault.id)

            return {
                "status": "success",
                "notes_synced": total_synced,
            }

        except Exception as e:
            logger.error(f"Personal KB sync failed: {e}")
            return {"status": "error", "message": str(e)}


class CyberEmployeeBuilder:
    """
    赛博员工构建器
    通过 Obsidian + 知识图谱 + 个人记忆 构建个性化 AI 员工
    """

    def __init__(self, employee_id: str):
        self.employee_id = employee_id
        self.personal_rag = PersonalRAGEngine(employee_id=employee_id)

    def build_profile_prompt(self) -> str:
        """构建个性化系统提示词"""
        parts = []

        # 1. 基础角色设定
        parts.append("你是一位专属的赛博员工，深度了解这个用户。")

        # 2. 加载个人记忆
        from core.personal_knowledge import PersonalMemoryManager
        memory_manager = PersonalMemoryManager(self.employee_id)
        memory_context = memory_manager.build_memory_context()
        if memory_context:
            parts.append(memory_context)

        # 3. 加载知识图谱信息
        kg_context = self._build_kg_context()
        if kg_context:
            parts.append(kg_context)

        # 4. 加载 Obsidian 笔记摘要
        notes_context = self._build_notes_context()
        if notes_context:
            parts.append(notes_context)

        return "\n\n".join(parts)

    def _build_kg_context(self) -> str:
        """构建知识图谱上下文"""
        try:
            from core.personal_knowledge import KnowledgeGraphManager
            manager = KnowledgeGraphManager(self.employee_id)

            with get_db_session() as session:
                from sqlalchemy import select
                from database import PersonalKnowledgeGraphModel

                stmt = select(PersonalKnowledgeGraphModel).where(
                    PersonalKnowledgeGraphModel.employee_id == self.employee_id
                ).order_by(
                    PersonalKnowledgeGraphModel.importance_score.desc()
                ).limit(20)

                entities = list(session.execute(stmt).scalars().all())

            if not entities:
                return ""

            context = ["\n## 用户关注的知识领域:"]
            for e in entities[:10]:
                tags_str = ", ".join(e.tags) if e.tags else ""
                context.append(f"- **{e.entity_name}** ({e.entity_type}) {tags_str}")

            return "\n".join(context)

        except Exception as e:
            logger.error(f"Failed to build KG context: {e}")
            return ""

    def _build_notes_context(self) -> str:
        """构建 Obsidian 笔记上下文"""
        try:
            from core.personal_knowledge import PersonalNoteManager
            manager = PersonalNoteManager()

            with get_db_session() as session:
                from sqlalchemy import select, func
                from database import PersonalNoteModel

                stmt = select(
                    PersonalNoteModel.title,
                    PersonalNoteModel.tags,
                    PersonalNoteModel.summary,
                ).where(
                    PersonalNoteModel.employee_id == self.employee_id
                ).order_by(
                    PersonalNoteModel.last_modified.desc()
                ).limit(10)

                notes = list(session.execute(stmt).scalars().all())

            if not notes:
                return ""

            context = ["\n## 用户的 Obsidian 笔记:"]
            for note in notes:
                tags_str = ", ".join(note.tags) if note.tags else ""
                context.append(f"- {note.title} {tags_str}")

            return "\n".join(context)

        except Exception as e:
            logger.error(f"Failed to build notes context: {e}")
            return ""

    def learn_from_conversation(
        self,
        user_message: str,
        assistant_response: str,
    ):
        """从对话中学习，更新记忆和知识"""
        try:
            from core.personal_knowledge import PersonalMemoryManager, KnowledgeGraphExtractor
            import json

            memory_manager = PersonalMemoryManager(self.employee_id)

            user_keywords = self._extract_entities(user_message)
            for entity in user_keywords:
                memory_manager.add_memory(
                    memory_type="interest",
                    memory_key=f"interest_{entity}",
                    content=f"用户询问过: {entity}",
                    summary=f"用户关注: {entity}",
                    confidence=0.7,
                    source_messages=[user_message],
                )

            if any(kw in user_message.lower() for kw in ["我喜欢", "我的", "我是", "我的工作"]):
                memory_manager.add_memory(
                    memory_type="profile",
                    memory_key="user_profile",
                    content=user_message,
                    summary=self._summarize_profile(user_message),
                    confidence=0.8,
                    source_messages=[user_message],
                )

            logger.info(f"Learned from conversation for employee {self.employee_id}")

        except Exception as e:
            logger.error(f"Failed to learn from conversation: {e}")

    def _extract_entities(self, text: str) -> List[str]:
        """提取实体"""
        import re
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+\d+)?)',
            r'([\w]{3,}(?:技术|系统|平台|工具|软件|硬件))',
        ]
        entities = []
        for pattern in patterns:
            entities.extend(re.findall(pattern, text))
        return list(set(entities))[:10]

    def _summarize_profile(self, text: str) -> str:
        """总结用户画像"""
        summary_prompt = f"从以下文本中提取关键的用户信息（职业、技能、兴趣等），用简洁的句子描述：\n\n{text}"
        try:
            from llm.llm_client import get_default_llm
            llm = get_default_llm()
            if llm:
                response = llm.chat([
                    {"role": "user", "content": summary_prompt}
                ])
                return response.content[:200] if response else ""
        except:
            pass
        return text[:100]


def get_personal_rag_engine(employee_id: str = None) -> PersonalRAGEngine:
    """获取个人 RAG 引擎"""
    return PersonalRAGEngine(employee_id=employee_id)


def get_cyber_employee_builder(employee_id: str) -> CyberEmployeeBuilder:
    """获取赛博员工构建器"""
    return CyberEmployeeBuilder(employee_id)
